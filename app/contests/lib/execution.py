"""
author: Derek McMahon
created: 11/13/2016

execution.py is concerned with the compilation and execution of C++ and Java files on the fly (the output of the program is returned as a string, but compiled and/or object files are deleted upon completion).
"""


import os
from subprocess import Popen, PIPE
import tempfile
import shutil
from threading import Timer

dir_path = os.path.dirname(os.path.realpath(__file__))

#Returns a return code and the output of the program or an error message
def execute_code(submission_file, original_filename, input_file, timeout=5):
    file_name, file_extension = os.path.splitext(submission_file.name)
    #Check if it's a Java file:
    if file_extension == '.java':
        return run_java(submission_file, original_filename, input_file, timeout)
    #Check if it's a c++ file:
    cpp_extensions = set(['.cpp', '.cc', '.C', '.cxx', '.c++'])
    if file_extension in cpp_extensions:
        return run_cpp(submission_file, input_file, timeout)
    #If it didn't have a proper extensions, can't compile and run it:
    return (1, "FILENAME ERROR: Must have a valid C++ or Java file extension")


#Returns the a return code and the output of the program or an error message as a tuple.
def run_java(submission_file, original_filename, input_file, timeout):
    temp_dirpath = tempfile.mkdtemp()
    file_name = original_filename
    with open(os.path.join(temp_dirpath, file_name), 'wb+') as destination:
        for chunk in submission_file.chunks():
            destination.write(chunk)
    compilation_result = Popen("javac " + os.path.join(temp_dirpath, file_name), shell=True, stdout=PIPE, stderr=PIPE)
    compiled_file = os.path.splitext(file_name)[0]
    output, error = compilation_result.communicate()
    retval = (1, 'Code timed out')
    if compilation_result.returncode !=0:
        retval = (1, ("COMPILATION ERROR:\n" + error.decode("utf-8").encode("utf-8")))
    else:
        if input_file != None and input_file.name != None:
            program_output = Popen("timeout " + str(timeout) + " java -cp " + temp_dirpath + " " + compiled_file + " < " + input_file.name, stdout=PIPE, stderr=PIPE, shell=True)
        else:
            program_output = Popen("timeout " + str(timeout) + " java -cp " + temp_dirpath + " " + compiled_file, stdout=PIPE, stderr=PIPE, shell=True)
        output, error = program_output.communicate()
        if program_output.returncode != 0:
            if error.decode("utf-8").encode("utf-8") != '':
                retval = (1, ("EXECUTION ERROR:\n" + error.decode("utf-8").encode("utf-8")))
        else:
            retval = (0, output.decode())
    shutil.rmtree(temp_dirpath)
    return retval

#Returns the a return code and the output of the program or an error message as a tuple.
def run_cpp(submission_file, input_file, timeout):
    temp_dirpath = tempfile.mkdtemp()
    file_name = os.path.basename(submission_file.name)
    with open(os.path.join(temp_dirpath, file_name), 'wb+') as destination:
        for chunk in submission_file.chunks():
            destination.write(chunk)
    compilation_result = Popen("/usr/bin/g++ " + os.path.join(temp_dirpath, file_name) + " -o " + os.path.join(temp_dirpath, 'a.out'), shell=True, stdout=PIPE, stderr=PIPE)
    output, error = compilation_result.communicate()
    retval = (1, 'Code timed out')
    if compilation_result.returncode != 0:
        retval = (1, ("COMPILATION ERROR:\n" + error.decode("utf-8").encode("utf-8")))
    else:
        if input_file != None and input_file.name != None:
            program_output = Popen("timeout " + str(timeout) + " " + os.path.join(temp_dirpath, './a.out' + ' < ' + input_file.name), shell=True, stdout=PIPE, stderr=PIPE)
        else:
            program_output = Popen("timeout " + str(timeout) + " " + os.path.join(temp_dirpath, './a.out'), shell=True, stdout=PIPE, stderr=PIPE)
        output, error = program_output.communicate()
        if program_output.returncode != 0:
            if error.decode("utf-8").encode("utf-8") != '':
                retval = (1, ("EXECUTION ERROR:\n" + error.decode("utf-8").encode("utf-8")))
        else:
            retval = (0, output.decode())
    shutil.rmtree(temp_dirpath)
    return retval
