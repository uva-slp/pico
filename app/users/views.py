from collections import namedtuple
import os
import shutil
import subprocess
import urllib

from django.db import connection
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, validate_email
from django.http import JsonResponse
from django.urls import reverse

from dal import autocomplete

from common.decorators import anonymous_required
from .forms import UserForm, LoginForm
from .models import User
from pico.secrets import DB_NAME
from pico.settings import GIT_ROOT, MNT_ROOT

@login_required
def index(request, user_id=None):
    user = None
    if user_id is not None:
        if User.objects.filter(id=user_id).exists():
            user = User.objects.get(id=user_id)
        else:
            return redirect(reverse('users:index'))

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
            try:
                UnicodeUsernameValidator()(username)
                request.user.username = username
                request.user.save()
                return JsonResponse({}, status=200)
            except ValidationError as err:
                return JsonResponse({'error': '; '.join(err.messages)}, status=201)

        if 'first_name' in request.POST:
            request.user.first_name = request.POST.get('first_name')
            request.user.save()
            return JsonResponse({}, status=200)

        if 'last_name' in request.POST:
            request.user.last_name = request.POST.get('last_name')
            request.user.save()
            return JsonResponse({}, status=200)

        if 'email' in request.POST:
            email = request.POST.get('email')
            if not email:
                request.user.email = email
                request.user.save()
                return JsonResponse({}, status=200)
            else:
                try:
                    validate_email(email)
                    request.user.email = email
                    request.user.save()
                    return JsonResponse({}, status=200)
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

            return JsonResponse({'error': 'Invalid theme URL.'}, status=201)

        return JsonResponse({}, status=400)

    return redirect(reverse('users:index', kwargs={'user_id':request.user.id}))

@login_required
def settings(request):
    context = None
    if request.user.is_staff:
        
        # Disk usage overall
        st = os.statvfs(MNT_ROOT)
        free = st.f_bavail * st.f_frsize
        total = st.f_blocks * st.f_frsize
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        usage_root = namedtuple('usage', 'total used free')(total, used, free)

        # Disk usage by repo/project
        usage_pico = int(subprocess.check_output('du -sb "%s"'%(GIT_ROOT), shell=True).split()[0].decode("utf-8"))
        
        # Disk usage by database
        cursor = connection.cursor()
        cursor.execute("SELECT sum( data_length + index_length ) " +
                       "FROM information_schema.TABLES " +
                       "WHERE table_schema=\"%s\";"%(DB_NAME))
        usage_db = int(cursor.fetchone()[0])
        
        context = {
            'disk_usage': {
                'total': usage_root.total,
                'free': usage_root.free,
                'pico': usage_pico,
                'db': usage_db,
                'other': usage_root.used-usage_pico-usage_db
            },
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
