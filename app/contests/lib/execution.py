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

#Returns a return code and the output of the program or an error message
def execute_code(Popen, submission_file, original_filename, input_file, allowed_languages, timeout=5):
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
    Popen("docker ps -f status=exited | awk '{ print $1, $2 }' | grep pccs | awk '{print $1 }' | xargs -I {} docker rm {}", shell=True)
    #Check if there was an error with the command to run the docker container:
    if error != '':
        return (1, "CONTAINER ERROR:\n" + error)
    #Parse the output of the docker container to get a tuple that has the return code of the executed program and the output of the program (or the error, if it did not execute successfully)
    retcode = int(output[:1])
    program_output = output[2:]
    return (retcode, program_output)


#Runs the given command to execute a compiled file
def execute_compiled_file(Popen, command, input_file):
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
    compilation_result = Popen("javac " + os.path.join("code", file_name), shell=True, stdout=PIPE, stderr=PIPE)
    compiled_file = os.path.splitext(file_name)[0]
    output, error = compilation_result.communicate()
    if compilation_result.returncode:
        return (1, ("COMPILATION ERROR:\n" + str(error.decode("utf-8"))))
    command = "timeout " + str(timeout) + " java -cp " + "code/" + " " + compiled_file
    return execute_compiled_file(Popen, command, input_file)


#Returns the a return code and the output of the program or an error message as a tuple.
def run_cpp(Popen, file_name, input_file, timeout):
    compilation_result = Popen("/usr/bin/g++ " + os.path.join("code", file_name) + " -o " + os.path.join("code", 'a.out'), shell=True, stdout=PIPE, stderr=PIPE)
    output, error = compilation_result.communicate()
    if compilation_result.returncode:
        return(1, ("COMPILATION ERROR:\n" + str(error.decode("utf-8"))))
    command = "timeout " + str(timeout) + " " + os.path.join("code", './a.out')
    return execute_compiled_file(Popen, command, input_file)


#Returns the a return code and the output of the program or an error message as a tuple.
def run_python(Popen, file_name, input_file, timeout):
    command = "timeout " + str(timeout) + " python " + os.path.join("code", file_name)
    return execute_compiled_file(Popen, command, input_file)


def docker_container_code(Popen, args):
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
    result = docker_container_code(Popen, sys.argv)
    print(str(result[0]) + ',' + str(result[1]), end='')
