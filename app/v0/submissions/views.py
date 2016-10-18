from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render
from .forms import UploadCodeForm
from contests.models import Question

import os
import subprocess

dir_path = os.path.dirname(os.path.realpath(__file__))

def choose_question(request):
    all_questions = Question.objects.all()
    return render(request, 'submissions/choose_question.html', {'questions': all_questions})


def upload_code(request, question_id):
    question = Question.objects.get(id=question_id)
    if request.method == 'POST':
        form = UploadCodeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            execute_code(request.FILES['code_file'], form.instance.submission_id)
            return HttpResponseRedirect(reverse('submissions:success'))
    else:
        form = UploadCodeForm(initial = {'question': question})
    return render(request, 'submissions/upload_page.html', {'form': form, 'question': question})


#Returns True if executed successfully, false otherwise
def execute_code(file, submission_id):
    file_name = file.name
    copy_code_to_uploads_directory(file, submission_id)
    #Check if it's a Java file:
    if file_name.endswith('.java'):
        run_java(file, submission_id)
        return True
    #Check if it's a c++ file:
    cpp_extensions = ['.cpp', '.cc', '.C', '.cxx', '.c++']
    for extension in cpp_extensions:
        if file_name.endswith(extension):
            run_cpp(file, submission_id)
            return True
    #If it didn't have a proper extensions, can't compile it:
    return False


def copy_code_to_uploads_directory(file, submission_id):
    path = os.path.join(dir_path, 'uploads/submission' + str(submission_id) + '/')
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.makedirs(os.path.dirname(path))
        #In case there is a race condition
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise
    with open(os.path.join(path, file.name), 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)


def run_java(file, submission_id):
    file_name = file.name
    path = os.path.join(dir_path,  'uploads/submission'+str(submission_id)+'/')
    compiled_file = os.path.splitext(file_name)[0]
    subprocess.call("rm -f " + os.path.join(path, compiled_file), shell=True)
    retcode = subprocess.call("javac " + os.path.join(path, file_name), shell=True)
    if retcode:
        print("failed to compile" + file_name)
    retcode = subprocess.call("java -cp " + path + " " + compiled_file + ' > ' + os.path.join(path, 'output.txt'), shell=True)


def run_cpp(file, submission_id):
    file_name = file.name
    path = os.path.join(dir_path,  'uploads/submission'+str(submission_id)+'/')
    subprocess.call("rm -f " + os.path.join(path + "/a.out"), shell=True)
    retcode = subprocess.call("/usr/bin/g++ " + os.path.join(path, file_name) + " -o " + os.path.join(path, 'a.out'), shell=True)
    if retcode:
        print("failed to compile " + file_name)
    retcode = subprocess.call(os.path.join(path, './a.out') + ' > ' + os.path.join(path, 'output.txt'), shell=True)

    
def success(request):
    return HttpResponse('File uploaded successfully!')
