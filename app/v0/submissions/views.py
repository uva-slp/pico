from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from .forms import UploadCodeForm

import os
import subprocess

dir_path = os.path.dirname(os.path.realpath(__file__))

def upload_code(request):
    if request.method == 'POST':
        form = UploadCodeForm(request.POST, request.FILES)
        file = request.FILES['file']
        copy_code_to_uploads_directory(file)
        execute(file)
        if form.is_valid():
            save_submission(file)
            return HttpResponseRedirect('/submissions/success')
    else:
        form = UploadCodeForm()
    return render(request, 'submissions/upload_page.html', {'form': form})


#Returns True if executed successfully, false otherwise
def execute(file):
    file_name = file.name
    #Check if it's a Java file:
    if file_name.endswith('.java'):
        run_java(file)
        return True
    #Check if it's a c++ file:
    cpp_extensions = ['.cpp', '.cc', '.C', '.cxx', '.c++']
    for extension in cpp_extensions:
        if file_name.endswith(extension):
            run_cpp(file)
            return True
    #If it didn't have a proper extensions, can't compile it:
    return False


def copy_code_to_uploads_directory(file):
    with open(os.path.join(dir_path, 'uploads/') + file.name, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def run_java(file):
    file_name = file.name
    subprocess.call("rm -f ./a.out", shell=True)
    retcode = subprocess.call("javac " + os.path.join(dir_path, 'uploads/') + file_name, shell=True)
    if retcode:
        print("failed to compile" + file_name)
    compiled_file = os.path.splitext(file_name)[0]
    retcode = subprocess.call("java -cp " + os.path.join(dir_path, 'uploads/') + " " + compiled_file, shell=True)


def run_cpp(file):
    file_name = file.name
    subprocess.call("rm -f ./a.out", shell=True)
    retcode = subprocess.call("/usr/bin/g++ " + os.path.join(dir_path, 'uploads/') + file_name + " -o " + os.path.join(dir_path, 'uploads/a.out'), shell=True)
    if retcode:
        print("failed to compile " + file_name)
    retcode = subprocess.call(os.path.join(dir_path, "uploads/./a.out"), shell=True)


def save_submission(f):
    #This is where the submission will be saved to a model
    print("Actually, submissions will probably be saved directly with a model form")

def success(request):
    return HttpResponse('File uploaded successfully!')
