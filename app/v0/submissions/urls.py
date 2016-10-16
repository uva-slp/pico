from django.conf.urls import url

from . import views

app_name = 'submissions'
urlpatterns = [
    url(r'^$', views.upload_code, name='upload_code'),
    url(r'^success$', views.success, name='success'),
]
