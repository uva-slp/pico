from django.conf.urls import patterns, include, url

import views


urlpatterns = patterns('',
    url(r'^$', views.profile, name='home'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^retrievepw/$', views.retrieve_password, name='retrieve_password'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^reset/done/$', views.password_reset_complete, name='password_reset_complete'),
    url(r'resetpw/$', views.reset_password, name='reset_password'),
    url(r'resetpw/done/$', views.reset_password_done, name='reset_password_done'),
    url(r'^register/$', views.register, name='register'),
    url(r'^confirm/(?P<activation_key>\w+)/', views.register_confirm, name='register_confirm'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'', include('django.contrib.auth.urls')),

)