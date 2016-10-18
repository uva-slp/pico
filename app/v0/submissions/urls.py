from django.conf.urls import url

from . import views

app_name = 'submissions'
urlpatterns = [
    url(r'^$', views.choose_question, name='choose_question'),
    url(r'^upload/(?P<question_id>[0-9]+)/$', views.upload_code, name='upload_code'),
    url(r'^upload/success$', views.success, name='success'),
]
