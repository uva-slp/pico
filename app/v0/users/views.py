from django.conf import settings

from django.shortcuts import render, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404, resolve_url

from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext as _

from models import UserProfile

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
import hashlib, datetime, random
from django.utils import timezone
from django.contrib.auth import (REDIRECT_FIELD_NAME, login as auth_login,
                                 logout as auth_logout)

from django.template.response import TemplateResponse
from django.utils.http import is_safe_url


# Create your views here.

@sensitive_post_parameters()
@csrf_protect
@never_cache
def register(request, creation_form=UserCreationForm, extra_context=None):
    form = creation_form(request.POST or None)
    if request.method == "POST":
        # Add User Model instance here
        if form.is_valid():
            if not request.POST.get("email"):
                error = "The email field is required!"
                return render(request, "myregistration/register.html", {'message': error})
            # create the user
            user = form.save()
            # user.is_active = False
            email = request.POST.get("email")
            user.email = email
            user.save()
            profile = UserProfile(user=user)
            username = form.cleaned_data['username']
            random_string = str(random.random()).encode('utf8')
            salt = hashlib.sha1(random_string).hexdigest()[:5]
            salted = (salt + email).encode('utf8')
            activation_key = hashlib.sha1(salted).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)
            profile.activation_key = activation_key
            profile.key_expires = key_expires
            profile.save()

            # Send email with activation key
            email_subject = 'Account confirmation'
            email_body = "Hey %s, thanks for signing up. To activate your account, click this link within" \
                         "48hours http://127.0.0.1:8000/users/confirm/%s" % (username, activation_key)

            send_mail(email_subject, email_body, 'pccsuva@gmail.com', [email], fail_silently=False)

            return render(request, "myregistration/register_success.html")
    context = {
        'form': form,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, "myregistration/register.html", context)


def register_confirm(request, activation_key):
    # if user already logged in, redirect to some other url
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))

    profile = get_object_or_404(UserProfile, activation_key=activation_key)

    if profile.key_expires < timezone.now():
        email = profile.user.email
        # email = "viviancaas@gmail.com"
        username = profile.user.username
        random_string = str(random.random()).encode('utf8')
        salt = hashlib.sha1(random_string).hexdigest()[:5]
        salted = (salt + email).encode('utf8')
        activation_key = hashlib.sha1(salted).hexdigest()
        key_expires = datetime.datetime.today() + datetime.timedelta(2)
        profile.activation_key = activation_key
        profile.key_expires = key_expires
        profile.save()
        email_subject = 'Account confirmation'
        email_body = "Hey %s, thanks for signing up. To activate your account, click this link within" \
                     "48hours: http://127.0.0.1:8000/users/confirm/%s" % (username, activation_key)

        send_mail(email_subject, email_body, 'viviancaas@gmail.com', [email], fail_silently=False)
        return render(request, "myregistration/confirm_expired.html")
    else:
        # user = profile.user
        # user.is_active = True
        profile.suspended = False
        profile.save()
        return render(request, "myregistration/confirm.html")


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login(request, template_name='myregistration/login.html',
          redirect_field_name=REDIRECT_FIELD_NAME,
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        if request.POST.get("login"):
            form = authentication_form(request, data=request.POST)
            if form.is_valid():
                # Ensure the user-originating redirection url is safe.
                if not is_safe_url(url=redirect_to, host=request.get_host()):
                    redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

                # Okay, security check complete. Log the user in.
                profile = UserProfile.objects.filter(user=form.get_user())

                if len(profile) is 0:
                    context = {
                        'form': form,
                        redirect_field_name: redirect_to,
                    }
                    if extra_context is not None:
                        context.update(extra_context)
                    return TemplateResponse(request, template_name, context,

                                            current_app=current_app)
                profile = profile[0]
                if profile.is_suspended:
                    error_type = 5
                    return render(request, 'error_page.html', {'t': error_type})
                    # return render(request, 'myregistration/suspended.html')

                auth_login(request, form.get_user())

                return HttpResponseRedirect(redirect_to)
        elif request.POST.get("forgetP"):
            return HttpResponseRedirect(reverse('users:retrieve_password'))
        else:
            error_type = 4
            return render(request, 'error_page.html', {'t': error_type})

    form = authentication_form(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def logout(request, next_page=None,
           template_name='myregistration/logged_out.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           current_app=None, extra_context=None):
    """
    Logs out the user and displays 'You are logged out' message.
    """
    auth_logout(request)

    if next_page is not None:
        next_page = resolve_url(next_page)

    if (redirect_field_name in request.POST or
                redirect_field_name in request.GET):
        next_page = request.POST.get(redirect_field_name,
                                     request.GET.get(redirect_field_name))
        # Security check -- don't allow redirection to a different host.
        if not is_safe_url(url=next_page, host=request.get_host()):
            next_page = request.path

    if next_page:
        # Redirect to this page until the session has been cleared.
        return HttpResponseRedirect(next_page)

    current_site = get_current_site(request)
    context = {
        'site': current_site,
        'site_name': current_site.name,
        'title': _('Logged out')
    }
    if extra_context is not None:
        context.update(extra_context)
    return TemplateResponse(request, template_name, context,
                            current_app=current_app)


def retrieve_password(request):
    if request.method == "POST":
        if request.POST.get("cancel"):
            return HttpResponseRedirect(reverse('users:login'))
        elif request.POST.get("resetP"):
            request_name = request.POST.get("username")
            email_address = request.POST.get("email")
            user_filter = UserProfile.objects.filter(user__username=request_name)
            if len(user_filter) == 0:
                error = "This username does not exist!"
                return render(request, 'myregistration/password_reset_form.html', {'message': error})
            else:
                profile = user_filter[0]
                if profile.user.email == email_address:
                    current_site = get_current_site(request)
                    token_generator = default_token_generator

                    c = {
                        'email': email_address,
                        'domain': current_site.domain,
                        'site_name': current_site.name,
                        'uid': urlsafe_base64_encode(force_bytes(profile.user.pk)),
                        'user_prof': profile,
                        'token': token_generator.make_token(profile.user),
                        'protocol': 'http',
                    }
                    subject = 'Password Reset'
                    email = render_to_string('myregistration/password_reset_email.html', c)
                    send_mail(subject, email, 'pccsuva@gmail.com', [profile.user.email], fail_silently=False)
                    return render(request, 'myregistration/password_reset_done.html')
                else:
                    error = "The email address you entered is not compatible with the username!"
                    return render(request, 'myregistration/password_reset_form.html', {'message': error})
        else:
            error_type = 4
            return render(request, 'error_page.html', {'t': error_type})
    return render(request, 'myregistration/password_reset_form.html')


def password_reset_confirm(request, uidb64, token):
    uid = urlsafe_base64_decode(uidb64)
    user = UserProfile.objects.filter(user__pk=uid)

    if len(user) == 0:
        validlink = False
        # return render(request, 'myregistration/password_reset_confirm.html', {'validlink': validlink})
    else:
        profile = user[0]
        if default_token_generator.check_token(profile.user, token):
            validlink = True
        else:
            validlink = False
            # validlink = True
    if request.method == 'POST':
        password1 = request.POST.get("new_password1")
        password2 = request.POST.get("new_password2")
        if len(password1) == 0:
            error = "Error: your password is empty"
            return render(request, 'myregistration/password_reset_confirm.html',
                          {'validlink': validlink, 'message': error,
                           'uidb64': uidb64, 'token': token})
        elif password1 != password2:
            error = "Error: the two password you entered do not match"
            return render(request, 'myregistration/password_reset_confirm.html',
                          {'validlink': validlink, 'message': error,
                           'uidb64': uidb64, 'token': token})
        else:
            profile.user.set_password(password1)
            profile.user.save()
            profile.save()
            return HttpResponseRedirect(reverse('users:password_reset_complete'))
    return render(request, 'myregistration/password_reset_confirm.html', {'validlink': validlink, 'uidb64': uidb64,
                                                                          'token': token})


def password_reset_complete(request):
    return render(request, 'myregistration/password_reset_complete.html')


def reset_password(request):
    if request.user.is_active:
        profile = UserProfile.objects.filter(user=request.user)[0]
    else:
        profile = None

    if request.method == 'POST':
        old_password = request.POST.get("old_password")
        new_password1 = request.POST.get("new_password1")
        new_password2 = request.POST.get("new_password2")
        if not profile.user.check_password(old_password):
            error = "Your old password was incorrect. Please try again"
            return render(request, 'myregistration/password_change_form.html', {'message': error})
        elif new_password1 != new_password2:
            error = "The two new password you entered do not match. Please try again."
            return render(request, 'myregistration/password_change_form.html', {'message': error})
        else:
            profile.user.set_password(new_password1)
            profile.user.save()
            profile.save()
            return HttpResponseRedirect(reverse('users:reset_password_done'))
    return render(request, 'myregistration/password_change_form.html')


def reset_password_done(request):
    return render(request, 'myregistration/password_change_done.html')


@login_required(login_url="/users/login/")
def profile(request):
    # This code allows for an admin link on the user profile page.
    if request.user.is_active:
        profile = UserProfile.objects.filter(user=request.user)[0]
    else:
        profile = None

    return render(request, 'user_profile.html', {'prof': profile})