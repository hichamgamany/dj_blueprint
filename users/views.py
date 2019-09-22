from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.contrib.auth.views import *
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from users.tokens import account_activation_token
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm


def sign_up(request):
    template_name = 'users/register.html'
    title = 'Sign Up'
    if request.user.is_authenticated:
        messages.warning(request, 'You are already authenticated', extra_tags='warning')
        return redirect('profile')
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('users/messages/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            messages.success(request, 'An email has been sent to you for confirmation', extra_tags='success')
            return redirect('registration_confirm')
    else:
        form = UserRegisterForm()

    context = {
        'form': form,
        'title': title
    }

    return render(request, template_name, context)


def registration_confirmation(request):
    title = 'Registration Confirmation'
    template_name = 'users/registration_confirmation.html'
    context = {'title': title}
    return render(request, template_name, context)


def activation_done(request):
    title = 'Account Activated'
    template_name = 'users/account_activation_confirmation.html'
    messages.success(request, 'Congratulations, Your account has been activated', extra_tags='success')
    context = {'title': title}
    return render(request, template_name, context)


def activation_failed(request):
    title = 'Activation Failed'
    template_name = 'users/activation_failed.html'
    messages.error(request, 'Your Activation has failed! invalid token', extra_tags='danger')
    context = {'title': title}
    return render(request, template_name, context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('activation_done')
    else:
        return redirect('activation_failed')


class UserLoginView(SuccessMessageMixin, LoginView):
    title = 'SignIn'
    template_name = 'users/sign_in.html'
    redirect_authenticated_user = True
    success_message = 'You are successfully logged in'
    extra_context = {
        'title': title
    }


class UserLogoutView(SuccessMessageMixin, LogoutView):
    template_name = 'users/logout.html'


class UserPasswordResetView(PasswordResetView):
    title = 'Password Reset'
    template_name = 'users/password_reset.html'
    extra_context = {
        'title': title
    }


class UserPasswordResetDoneView(PasswordResetDoneView):
    title = 'Link sent'
    template_name = 'users/password_reset_done.html'
    extra_context = {'title': title}


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    title = 'Confirm Password Reset'
    template_name = 'users/password_reset_confirm.html'


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    title = 'Password Reset Complete'
    template_name = 'users/password_reset_complete.html'


@login_required
def profile_view(request):
    template_name = 'users/profile.html'
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'profile updated successfully', extra_tags="success")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, template_name, context)
