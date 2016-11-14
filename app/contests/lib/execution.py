"""
author: Derek McMahon
created: 11/13/2016

execution.py is concerned with the compilation and execution of C++ and Java files on the fly (the output of the program is returned as a string, but compiled and/or object files are deleted upon completion).
"""


import os
from subprocess import Popen, PIPE
import tempfile
import shutil

dir_path = os.path.dirname(os.path.realpath(__file__))


def execute_code(file):
    file_name, file_extension = os.path.splitext(file.name)
    #Check if it's a Java file:
    if file_extension == '.java':
        return run_java(file)
    #Check if it's a c++ file:
    cpp_extensions = set(['.cpp', '.cc', '.C', '.cxx', '.c++'])
    if file_extension in cpp_extensions:
        return run_cpp(file)
    #If it didn't have a proper extensions, can't compile and run it:
    return "Must have a valid C++ or Java file extension"


def run_java(file):
    temp_dirpath = tempfile.mkdtemp()
    file_name = file.name
    with open(os.path.join(temp_dirpath, file_name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    compilation_result = Popen("javac " + os.path.join(temp_dirpath, file_name), shell=True, stdout=PIPE, stderr=PIPE)
    compiled_file = os.path.splitext(file_name)[0]
    output, error = compilation_result.communicate()
    retval = ''
    if compilation_result.returncode !=0:
        retval = "THE ERROR IS: " + str(error.decode("utf-8"))
    else:
        program_output = Popen("java -cp " + temp_dirpath + " " + compiled_file, shell=True, stdout=PIPE, stderr=PIPE)
        output, error = program_output.communicate()
        retval = output
    shutil.rmtree(temp_dirpath)
    return retval


def run_cpp(file):
    temp_dirpath = tempfile.mkdtemp()
    file_name = file.name
    with open(os.path.join(temp_dirpath, file_name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    compilation_result = Popen("/usr/bin/g++ " + os.path.join(temp_dirpath, file_name) + " -o " + os.path.join(temp_dirpath, 'a.out'), shell=True, stdout=PIPE, stderr=PIPE)
    output, error = compilation_result.communicate()
    retval = ''
    if compilation_result.returncode !=0:
        retval = "THE ERROR IS: " + str(error.decode("utf-8"))
    else:
        program_output = Popen(os.path.join(temp_dirpath, './a.out'), shell=True, stdout=PIPE, stderr=PIPE)
        output, error = program_output.communicate()
        retval = output
    shutil.rmtree(temp_dirpath)
    return retval
