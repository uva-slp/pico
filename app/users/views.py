from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, validate_email
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from dal import autocomplete

from common.decorators import anonymous_required
from .forms import UserForm, LoginForm
from .lib import storage
from .models import User


@login_required
def view(request, user_id=None):
    user = None
    if user_id is not None:
        if User.objects.filter(id=user_id).exists():
            user = User.objects.get(id=user_id)
        else:
            return redirect(reverse('users:view'))

    return render(
        request,
        'users/index.html',
        {
            'user': user,
        },
    )

@anonymous_required
def register(request):
	if request.method == 'POST':
		user_form = UserForm(data=request.POST)

		if user_form.is_valid():
			user = user_form.save(commit=False)
			user.set_password(user.password)
			user.save()

			auth_login(request, user)

			return redirect(reverse('home'))
	else:
		user_form = UserForm()

	return render(
		request,
		'users/register.html',
		{'user_form': user_form})

@anonymous_required
def login(request):
	if request.method == 'POST':
		login_form = LoginForm(data=request.POST)

		if login_form.is_valid():
			auth_login(request, login_form.user_cache)
			return redirect(reverse('home'))

	else:
		login_form = LoginForm()

	return render(
		request,
		'users/login.html',
		{'login_form': login_form})

def logout(request):
	if request.user.is_authenticated():
		auth_logout(request)
	return redirect(reverse('index'))

@login_required
def edit(request):
    if request.method == 'POST':

        if 'username' in request.POST:
            username = request.POST.get('username')
            # Check if username is taken
            if User.objects.filter(username=username).exclude(pk=request.user.pk).exists():
                return JsonResponse({'error': 'Username already in use.'}, status=201)
            try:
                UnicodeUsernameValidator()(username)
                request.user.username = username
                request.user.save()
                return JsonResponse({'val':username}, status=200)
            except ValidationError as err:
                return JsonResponse({'error': '; '.join(err.messages)}, status=201)

        if 'first_name' in request.POST:
            request.user.first_name = request.POST.get('first_name')
            request.user.save()
            return JsonResponse({'val':request.user.first_name}, status=200)

        if 'last_name' in request.POST:
            request.user.last_name = request.POST.get('last_name')
            request.user.save()
            return JsonResponse({'val':request.user.last_name}, status=200)

        if 'email' in request.POST:
            email = request.POST.get('email')
            if not email:
                request.user.email = email
                request.user.save()
                return JsonResponse({'val':email}, status=200)
            else:
                try:
                    validate_email(email)
                    request.user.email = email
                    request.user.save()
                    return JsonResponse({'val':email}, status=200)
                except ValidationError as err:
                    return JsonResponse({'error': '; '.join(err.messages)}, status=201)

        if 'theme' in request.POST:
            theme = request.POST.get('theme')
            
            # Use default
            if not theme:
                profile = request.user.get_profile()
                profile.theme = theme
                profile.save()
                return JsonResponse({'theme': static('bootstrap/css/bootstrap.min.css')}, status=200)
            
            # Use Bootswatch theme
            try:
                URLValidator()(theme)
                if not theme.endswith('.css'):
                    raise ValidationError('URL must refer to a CSS file.')
                profile = request.user.get_profile()
                profile.theme = theme
                profile.save()
                return JsonResponse({'theme': theme}, status=200)
            except ValidationError as err:
                return JsonResponse({'error': '; '.join(err.messages)}, status=201)

        return JsonResponse({}, status=400)

    return redirect(reverse('users:view', kwargs={'user_id':request.user.id}))

@login_required
def settings(request):
    context = {}
    if request.user.is_staff:
        usage_root = storage.usage_root()
        usage_pico = storage.usage_pico()
        usage_db = storage.usage_db()
        context['disk_usage'] = {
            'total': usage_root.total,
            'free': usage_root.free,
            'pico': usage_pico,
            'db': usage_db,
            'other': usage_root.used-usage_pico-usage_db
        }
    return render(request, 'users/settings.html', context)

@login_required
def password_change(request):
	if request.method == 'POST':
		password_change_form = PasswordChangeForm(request.user, data=request.POST)

		if password_change_form.is_valid():
			password_change_form.save()
			update_session_auth_hash(request, password_change_form.user)
			return redirect(reverse('home'))

	else:
		password_change_form = PasswordChangeForm(request.user)

	return render(
		request,
		'users/password_change.html',
		{'password_change_form': password_change_form})

class UserAutocomplete(autocomplete.Select2QuerySetView):

    def get_queryset(self):     
        if not self.request.user.is_authenticated():
            return User.objects.none()
        
        qs = User.objects.all()
        if self.q:
            qs = qs.filter(username__istartswith=self.q)

        return qs
