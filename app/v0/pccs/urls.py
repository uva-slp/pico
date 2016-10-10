from django.conf.urls import include, url
from django.contrib import admin

from . import views

urlpatterns = [
    # url(r'^', include('main.urls', namespace='main')),
    url(r'^admin/', admin.site.urls),
    url(r'^github-hook$', views.github_hook, name='github-hook'),
    url(r'^$', views.index, name='index'),
]