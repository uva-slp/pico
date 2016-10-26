from django.conf.urls import include, url
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete

from . import views

urlpatterns = [
	url(r'^register$', views.register, name='register'),
	url(r'^login$', views.login, name='login'),
	url(r'^logout$', views.logout, name='logout'),
	url(r'^passwordchange$', views.password_change, name='password_change'),
    url(r'^password/reset/$', password_reset,
        {'post_reset_redirect' : '/password/reset/done/'},
        name="password_reset"),
    url(r'^password/reset/done/$', password_reset_done, name='password_reset_done'),
    url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        password_reset_confirm,
        {'post_reset_redirect' : '/password/done/'},
		name='password_reset_confirm'),
    url(r'^password/done/$',
        password_reset_complete
		, name='password_done'),
]
