from django.conf import settings
from django.shortcuts import redirect

def anonymous_required(view_func, redirect_url=None):
	return AnonymousRequired(view_func, redirect_url)

class AnonymousRequired(object):
	def __init__(self, view_func, redirect_url):
		if redirect_url is None:
			redirect_url = settings.LOGIN_REDIRECT_URL
		self.view_func = view_func
		self.redirect_url = redirect_url

	def __call__(self, request, *args, **kwargs):
		if request.user is not None and request.user.is_authenticated():
			return redirect(self.redirect_url)
		return self.view_func(request, *args, **kwargs)
