"""
author: Derek McMahon
created: 11/13/2016

execution.py is concerned with the compilation and execution of C++ and Java files on the fly (the output of the program is returned as a string, but compiled and/or object files are deleted upon completion). Since using VMs would be too slow for our purposes, the code is executed in Docker containers to provide some level of sandboxing although it is not perfectly secure (See https://docs.docker.com/engine/security/security/).
"""

from __future__ import print_function
import os
import sys
from subprocess import Popen, PIPE
import tempfile
import shutil
import ast

dir_path = os.path.dirname(os.path.realpath(__file__)) 

def execute_code(Popen, submission_file, original_filename, input_file, allowed_languages, timeout=5):
    """Executes the cpp, Java, or Python code in a Docker container (if the language is allowed).

    Args:
        Popen: A class that can execute subprocess commands.
        submission_file: A Django file containing the code to be executed.
        original_filename: The name of the file before being automatically made unique by the Django framework (important for Java files, where the whole file name matters).
        input_file: The file to be read as stdin in the program.
        allowed_languages: A list of a combination of the integers 1, 2, and 3 indicating which languages are allowed (1=Java, 2=C++, 3=Python).
        timeout: The maximum amount of time the code is given to execute.

    Returns:
        A tuple containing an integer return code (0=success, else failure) and a string of the output of the executed program (or error message).

    """
    #Get rid of white space in allowed_languages so it can be passed as a command line arg
    allowed_languages = "".join(allowed_languages.split())
    if not (submission_file and original_filename):
        return (1, "FILENAME ERROR: No file name given.")
    #Create a temporary directory to mount on the docker container
    temp_dirpath = tempfile.mkdtemp()
    file_name = original_filename
    #Copy the code file into the temporary directory
    with open(os.path.join(temp_dirpath, file_name), 'wb+') as destination:
        for chunk in submission_file.chunks():
            destination.write(chunk)
    docker_command = ("docker run -v " + temp_dirpath + ":/code dmm7aj/pccs python /code/execution.py " + file_name + " " + allowed_languages + " " + str(timeout)).split()
    Popen("cp " + os.path.join(dir_path, "execution.py") + " " + temp_dirpath, shell=True, stdout=PIPE, stderr=PIPE)
    #If this problem has an input file, put it in the temp directory and add it to the docker command:
    if input_file and input_file.name:
        with open(os.path.join(temp_dirpath, 'input.txt'), 'wb+') as destination:
            for chunk in input_file.chunks():
                destination.write(chunk)
        docker_command.append("input.txt")
    command = Popen(docker_command, stdin=PIPE, stderr=PIPE, stdout=PIPE, universal_newlines=True)
    output, error = command.communicate()
    #Delete the temporary directory and docker container
    shutil.rmtree(temp_dirpath)
    Popen("docker ps -f status=exited | awk '{ print $1, $2 }' | grep pccs | awk '{print $1 }' | xargs -I {} docker rm {}", shell=True, stdout=PIPE)
    #Check if there was an error with the command to run the docker container:
    if error != '':
        return (1, "CONTAINER ERROR:\n" + error)
    #Parse the output of the docker container to get a tuple that has the return code of the executed program and the output of the program (or the error, if it did not execute successfully)
    retcode = int(output[:1])
    program_output = output[2:]
    return (retcode, program_output)


def execute_compiled_file(Popen, command, input_file):
    """Runs the given command to execute a compiled Java, C++, or Python file.

    Args:
        Popen: A class that can execute subprocess commands.
        command: The string holding the command to execute the compiled file.
        input_file: The file to be read as stdin in the program.

    Returns:
        A tuple containing an integer return code (0=success, else failure) and a string containing the output of the program (or error message).

    """
    if input_file:
        program_output = Popen(command + " < " + os.path.join("code", input_file), stdout=PIPE, stderr=PIPE, shell=True)
    else:
        program_output = Popen(command, stdout=PIPE, stderr=PIPE, shell=True)
    output, error = program_output.communicate()
    if program_output.returncode:
        if str(error.decode("utf-8")) == '':
            return (1, 'CODE TIMED OUT')
        else:
            return (1, "EXECUTION ERROR:\n" + str(error.decode("utf-8")))
    else:
        return (0, output.decode())
    

#Returns the a return code and the output of the program or an error message as a tuple.
def run_java(Popen, file_name, input_file, timeout):
    """Runs the provided Java file.

    Args:
        Popen: A class that can execute subprocess commands.
        file_name: The name of the Java file to be compiled and executed.
        input_file: The file to be read as stdin in the program.
        timeout: The maximum amount of time the code is given to execute.

    Returns:
        A tuple containing an integer return code (0=success, else failure) and a string with the output of the executed program or an error message.

    """
    compilation_result = Popen("javac " + os.path.join("code", file_name), shell=True, stdout=PIPE, stderr=PIPE)
    compiled_file = os.path.splitext(file_name)[0]
    output, error = compilation_result.communicate()
    if compilation_result.returncode:
        return (1, ("COMPILATION ERROR:\n" + str(error.decode("utf-8"))))
    command = "timeout " + str(timeout) + " java -cp " + "code/" + " " + compiled_file
    return execute_compiled_file(Popen, command, input_file)


def run_cpp(Popen, file_name, input_file, timeout):
    """Runs the provided C++ file.

    Args:
        Popen: A class that can execute subprocess commands.
        file_name: The name of the C++ file to be compiled and executed.
        input_file: The file to be read as stdin in the program.
        timeout: The maximum amount of time the code is given to execute.

    Returns:
        A tuple containing an integer return code (0=success, else failure) and a string with the output of the executed program or an error message.

    """
    compilation_result = Popen("/usr/bin/g++ " + os.path.join("code", file_name) + " -o " + os.path.join("code", 'a.out'), shell=True, stdout=PIPE, stderr=PIPE)
    output, error = compilation_result.communicate()
    if compilation_result.returncode:
        return(1, ("COMPILATION ERROR:\n" + str(error.decode("utf-8"))))
    command = "timeout " + str(timeout) + " " + os.path.join("code", './a.out')
    return execute_compiled_file(Popen, command, input_file)


def run_python(Popen, file_name, input_file, timeout):
    """Runs the provided Python file.

    Args:
        Popen: A class that can execute subprocess commands.
        file_name: The name of the Python file to be compiled and executed.
        input_file: The file to be read as stdin in the program.
        timeout: The maximum amount of time the code is given to execute.

    Returns:
        A tuple containing an integer return code (0=success, else failure) and a string with the output of the executed program or an error message.

    """
    command = "timeout " + str(timeout) + " python " + os.path.join("code", file_name)
    return execute_compiled_file(Popen, command, input_file)


def docker_container_code(Popen, args):
    """Runs the provided code with the proper input. Note that this should only be run in a Docker container that has had the proper temporary file system mounted to it (which is set up in the function "execute_code()").

    Args:
        Popen: A class that can execute subprocess commands.
        args: The command line arguments indicating the currently running script name, the name of the code file to be executed, the allowed languages, the timeout, and the input file (if provided). They start from index 0 and are order as listed. 

    Returns:
        A tuple containing an integer return code (0=success, else failure) and a string with the output of the executed program or an error message.

    """
    if len(args) < 4:
        return(1, "FILENAME ERROR: No file name given.")
    file_name = args[1]
    allowed_languages = ast.literal_eval(args[2])
    timeout = int(args[3])
    input_file = None
    if len(args) > 4:
        input_file = args[4]
    file_prefix, file_extension = os.path.splitext(file_name)
    #Check if it's a Java file:
    if file_extension == '.java':
        if '1' in allowed_languages:
            return run_java(Popen, file_name, input_file, timeout)
        return (1, "LANGUAGE ERROR: Java submissions are not allowed in this contest")
    #Check if it's a c++ file:
    cpp_extensions = {'.cpp', '.cc', '.C', '.cxx', '.c++'}
    if file_extension in cpp_extensions:
        if '2' in allowed_languages:
            return run_cpp(Popen, file_name, input_file, timeout)
        return (1, "LANGUAGE ERROR: C++ submissions are not allowed in this contest")
    #Check if it's a python file:
    if file_extension == '.py':
        if '3' in allowed_languages:
            return run_python(Popen, file_name, input_file, timeout)
        return (1, "LANGUAGE ERROR: Python submissions are not allowed in this contest")
    #If it didn't have a proper extensions, have a default error:
    return (1, "FILENAME ERROR: Must have a valid C++, Java, or Python file extension")


if __name__ == "__main__":
    """This file (i.e. execution.py) is executed directly in a Docker container to run code. That causes this section to execute, which calls the docker_container_code() function that contains the logic to execute the provided Python, Java, or C++ file that is available in the volume mounted to the container in the execute_code() function.

    Args:
        sys.argv: The command line arguments indicating the currently running script name, the name of the code file to be executed, the allowed languages, the timeout, and the input file (if provided). They start from index 0 and are order as listed. 

    Returns:
        Does not (and cannot) return since it is not a function. Prints out the results of the executed code to be processed by the calling execute_code() function outside of the container. Prints the retcode and output separated by a comma.

    """
    result = docker_container_code(Popen, sys.argv)
    print(str(result[0]) + ',' + str(result[1]), end='')
