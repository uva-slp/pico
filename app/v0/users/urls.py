from django.conf.urls import patterns, include, url

import views


urlpatterns = patterns('',
    url(r'^$', views.profile, name='home'),
    url(r'^group_details/(\d+)/$', views.group_details, name='group_details'),
    url(r'^login/$', views.login, name='login'),
    url(r'^add_group_user/(\d+)/$', views.add_group_user, name='add_group_user'),
    url(r'^logout/$', views.logout, name='logout'),
    # url(r'^changepw/$', 'django.contrib.auth.views.password_change', name='password_change'),
    url(r'^retrievepw/$', views.retrieve_password, name='retrieve_password'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.password_reset_confirm,
        name='password_reset_confirm'),
    url(r'^reset/done/$', views.password_reset_complete, name='password_reset_complete'),
    url(r'resetpw/$', views.reset_password, name='reset_password'),
    url(r'resetpw/done/$', views.reset_password_done, name='reset_password_done'),
    url(r'^register/$', views.register, name='register'),
    # url(r'^register_success/$', views.register_success, name='register_success'),
    url(r'^confirm/(?P<activation_key>\w+)/', views.register_confirm, name='register_confirm'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^admin/$', views.admin_page, name='admin_page'),
    url(r'^admin/user/(\d+)/$', views.admin_user, name='admin_user'),
    url(r'^admin/delete/user/(\d+)/$', views.admin_deleteuser, name='admin_deleteuser'),
    url(r'^admin/modify/user/(\d+)/$', views.admin_makeadmin, name='admin_makeadmin'),
    url(r'^admin/suspend/user/(\d+)/$', views.admin_suspend, name='admin_suspend'),
    url(r'^admin/unsuspend/user/(\d+)/$', views.admin_unsuspend, name='admin_unsuspend'),
    url(r'^admin/group/(\d+)/$', views.admin_group, name='admin_group'),
    url(r'^admin/group/$', views.admin_creategroup, name='admin_creategroup'),
    url(r'^admin/group/(\d+)/adduser/$', views.admin_group_adduser, name='admin_group_adduser'),
    url(r'^admin/group/(\d+)/removeuser/(\d+)/$', views.admin_group_removeuser,
        name='admin_group_removeuser'),
    url(r'^admin/group/(\d+)/delete$', views.admin_group_delete, name='admin_group_delete'),
    url(r'^add_group/$', views.add_group, name='add_group'),
    url(r'', include('django.contrib.auth.urls')),

)