"""
author: Derek McMahon
created: 11/13/2016

execution.py is concerned with the compilation and execution of C++ and Java files on the fly (the output of the program is returned as a string, but compiled and/or object files are deleted upon completion). Since using VMs would be too slow for our purposes, the code is executed in Docker containers to provide some level of sandboxing although it is not perfectly secure (See https://docs.docker.com/engine/security/security/).
"""


import os
import sys
from subprocess import Popen, PIPE
import tempfile
import shutil

dir_path = os.path.dirname(os.path.realpath(__file__))
#TODO: Should use a Unix group called docker and add users so the password doesn't have to be hardcoded 

#Returns a return code and the output of the program or an error message
def execute_code(submission_file, original_filename, input_file, timeout=5):
    if not (submission_file and original_filename):
        return (1, "FILENAME ERROR: No file name given.")
    #Create a temporary directory to mount on the docker container
    temp_dirpath = tempfile.mkdtemp()
    file_name = original_filename
    with open(os.path.join(temp_dirpath, file_name), 'wb+') as destination:
        for chunk in submission_file.chunks():
            destination.write(chunk)
    #If this problem has an input file:
    if input_file and input_file.name:
        with open(os.path.join(temp_dirpath, 'input.txt'), 'wb+') as destination:
            for chunk in input_file.chunks():
                destination.write(chunk)
        Popen("cp " + os.path.join(dir_path, "execution.py") + " " + temp_dirpath, shell=True, stdout=PIPE, stderr=PIPE)
        docker_command = ("docker run -v " + temp_dirpath + ":/code dmm7aj/pccs python /code/execution.py " + file_name + " input.txt").split()
        command = Popen(docker_command, stdin=PIPE, stderr=PIPE, stdout=PIPE, universal_newlines=True)
    #If this problem does not have an input file:
    else:
        Popen("cp " + os.path.join(dir_path, "execution.py") + " " + temp_dirpath, shell=True, stdout=PIPE, stderr=PIPE)
        docker_command = ("docker run -v " + temp_dirpath + ":/code dmm7aj/pccs python /code/execution.py " + file_name).split()
        command = Popen(docker_command, stdin=PIPE, stderr=PIPE, stdout=PIPE, universal_newlines=True)
    output, error = command.communicate()
    #Delete the temporary directory
    shutil.rmtree(temp_dirpath)
    #Check if there was an error with the command to run the docker container:
    if error != '':
        return (1, "Container error:\n" + error)
    #Parse the output of the docker container to get a tuple that has the return code of the executed program and the output of the program (or the error, if it did not execute successfully)
    index = 1
    while index < len(output):
        if ord(output[index])-ord('0') > 9 or ord(output[index])-ord('0') < 0:
            retcode = int(output[0:index])
            program_output = output[index+1:len(output)-1]
            break
        index += 1
    return (retcode, program_output)


#Returns the a return code and the output of the program or an error message as a tuple.
def run_java(file_name, input_file, timeout):
    compilation_result = Popen("javac " + os.path.join("code", file_name), shell=True, stdout=PIPE, stderr=PIPE)
    compiled_file = os.path.splitext(file_name)[0]
    output, error = compilation_result.communicate()
    retval = (1, 'CODE TIMED OUT')
    if compilation_result.returncode:
        retval = (1, ("COMPILATION ERROR:\n" + str(error.decode("utf-8"))))
    else:
        if input_file:
            program_output = Popen("timeout " + str(timeout) + " java -cp " + "code/" + " " + compiled_file + " < " + os.path.join("code", input_file), stdout=PIPE, stderr=PIPE, shell=True)
        else:
            program_output = Popen("timeout " + str(timeout) + " java -cp " + "code/" + " " + compiled_file, stdout=PIPE, stderr=PIPE, shell=True)
        output, error = program_output.communicate()
        if program_output.returncode:
            if str(error.decode("utf-8")) != '':
                retval = (1, ("EXECUTION ERROR:\n" + str(error.decode("utf-8"))))
        else:
            retval = (0, output.decode())
    return retval


#Returns the a return code and the output of the program or an error message as a tuple.
def run_cpp(file_name, input_file, timeout):
    compilation_result = Popen("/usr/bin/g++ " + os.path.join("code", file_name) + " -o " + os.path.join("code", 'a.out'), shell=True, stdout=PIPE, stderr=PIPE)
    output, error = compilation_result.communicate()
    retval = (1, 'CODE TIMED OUT')
    if compilation_result.returncode:
        retval = (1, ("COMPILATION ERROR:\n" + str(error.decode("utf-8"))))
    else:
        if input_file:
            program_output = Popen("timeout " + str(timeout) + " " + os.path.join("code", './a.out') + ' < ' + os.path.join("code", input_file), shell=True, stdout=PIPE, stderr=PIPE)
        else:
            program_output = Popen("timeout " + str(timeout) + " " + os.path.join("code", './a.out'), shell=True, stdout=PIPE, stderr=PIPE)
        output, error = program_output.communicate()
        if program_output.returncode:
            if str(error.decode("utf-8")) != '':
                retval = (1, ("EXECUTION ERROR:\n" + str(error.decode("utf-8"))))
        else:
            retval = (0, output.decode())
    return retval


#Returns the a return code and the output of the program or an error message as a tuple.
def run_python(file_name, input_file, timeout):
    if input_file:
        execution_result = Popen("timeout " + str(timeout) + " python " + os.path.join("code", file_name) + " < " + os.path.join("code", input_file), shell=True, stdout=PIPE, stderr=PIPE)
    else:
        execution_result = Popen("timeout " + str(timeout) + " python " + os.path.join("code", file_name), shell=True, stdout=PIPE, stderr=PIPE)
    output, error = execution_result.communicate()
    retval = (1, 'CODE TIMED OUT')
    if execution_result.returncode:
        if str(error.decode("utf-8")) != '':
            retval = (1, ("EXECUTION ERROR:\n" + str(error.decode("utf-8"))))
    else:
        retval = (0, output.decode())
    return retval


if __name__ == "__main__":
    if len( sys.argv) < 2:
        print("1,FILENAME ERROR: No file name given.")
    else:
        input_file = None
        if len(sys.argv) > 2:
            input_file = sys.argv[2]
        file_name = sys.argv[1]
        file_prefix, file_extension = os.path.splitext(file_name)
        timeout = 5
        #If it didn't have a proper extensions, have a default error:
        result = (1, "FILENAME ERROR: Must have a valid C++ or Java file extension")
        #Check if it's a Java file:
        if file_extension == '.java':
            result = run_java(file_name, input_file, timeout)
        #Check if it's a c++ file:
        cpp_extensions = {'.cpp', '.cc', '.C', '.cxx', '.c++'}
        if file_extension in cpp_extensions:
            result = run_cpp(file_name, input_file, timeout)
        #Check if it's a python file:
        if file_extension == '.py':
            result = run_python(file_name, input_file, timeout)
        print(str(result[0]) + ',' + str(result[1]))
