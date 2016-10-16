from django.conf.urls import include, url
from django.contrib import admin

from pccs.views import *
from submissions import views

urlpatterns = [
    url(r'^submissions/', include('submissions.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', index, name='index'),
]
