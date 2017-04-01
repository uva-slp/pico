from django.conf.urls import include, url
from django.urls import reverse_lazy
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete

from . import views

urlpatterns = [
	url(r'^(?P<user_id>[0-9]*)/$', views.view, name='view'),
	url(r'^register$', views.register, name='register'),
	url(r'^login$', views.login, name='login'),
	url(r'^logout$', views.logout, name='logout'),
	url(r'^edit$', views.edit, name='edit'),
	url(r'^settings$', views.settings, name='settings'),
	url(r'^passwordchange$', views.password_change, name='password_change'),
	url(r'^password/reset/$', password_reset,
		{'template_name': 'users/password_reset/password_reset_form.html',
		'email_template_name': 'users/password_reset/password_reset_email.html',
		'post_reset_redirect' : reverse_lazy('users:password_reset_done')},
		name="password_reset"),
	url(r'^password/reset/done/$', password_reset_done,
		{'template_name': 'users/password_reset/password_reset_done.html'},
		name='password_reset_done'),
	url(r'^password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
		password_reset_confirm,
		{'template_name': 'users/password_reset/password_reset_confirm.html',
		'post_reset_redirect' : reverse_lazy('users:password_done')},
		name='password_reset_confirm'),
	url(r'^password/done/$',
		password_reset_complete,
		{'template_name': 'users/password_reset/password_reset_complete.html'},
		name='password_done'),
	url(r'^autocomplete$', views.UserAutocomplete.as_view(), name='autocomplete'),
]
