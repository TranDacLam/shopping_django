# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.auth import logout as auth_logout, login as auth_login
from django.contrib import messages
from forms import *
from registration.decorator import *

# Create your views here.

@is_authenticated
def login(request): 
    try:
        # Get nex page in url
        next_page = request.GET.get('next', '')

        result = {'next_page': next_page}

        if request.method == 'POST':
            login_form = LoginForm(request.POST, request=request)
            if login_form.is_valid():
                if next_page:
                    return redirect(next_page)
                return redirect(reverse('home'))
            else:
                result['errors'] = login_form.errors

        return render(request, 'registration/login.html', result)
            
    except Exception, e:
        print "Error Home: ", e
        raise Exception(
            "ERROR : Internal Server Error .Please contact administrator.")


def logout(request): 
    try:
        auth_logout(request)
        return redirect(reverse('home'))
    except Exception, e:
        print "Error Home: ", e
        raise Exception(
            "ERROR : Internal Server Error .Please contact administrator.")


@is_authenticated
def register(request): 
    try:
        if request.method == 'POST':
            form_register = RegisteForm(request.POST, request=request)
            if form_register.is_valid():
                form_register.save()
                messages.success(request, _(
                    'Register Account Successfully. Please Check Your Email and Active Account.'))
                return redirect(reverse('home'))
            else:
                print form_register.errors
                context = {}
                context['full_name'] = request.POST[
                    'full_name'] if 'full_name' in request.POST else None
                context['email'] = request.POST[
                    'email'] if 'email' in request.POST else None
                context['phone'] = request.POST[
                    'phone'] if 'phone' in request.POST else None
                context['gender'] = request.POST[
                    'gender'] if 'gender' in request.POST else None
                context['form'] = form_register
                return render(request, 'registration/register.html', context)

        return render(request, 'registration/register.html')
    except Exception, e:
        print "Error Home: ", e
        raise Exception(
            "ERROR : Internal Server Error .Please contact administrator.")


def confirm_activation(request, activation_key):
    """ Action Confirm User Activation"""
    print 'activation_key ', activation_key
    try:
        User = get_user_model()
        result = {}
        # User is exist in system then confirm has account
        if request.user.is_authenticated():
            return render(request, 'registration/activation_confirm.html', {'has_account': True})

        # Check activation key is valid
        try:
            user_account = get_object_or_404(User,
                                             activation_key=activation_key)
        except Exception:
            print "User Query activation_key does not exist."
            return render(request, 'registration/activation_confirm.html', {'key_wrong': True})

        # User have confirm link before then return flag active
        if user_account.is_active:
            return render(request, 'registration/activation_confirm.html', {'active': True})

        # Check key expires
        if user_account.key_expires < timezone.now():
            return render(request, 'registration/activation_confirm.html', {'expired': True})

        # hanlder active account
        user_account.is_active = True
        user_account.save()
        user_account.backend = 'django.contrib.auth.backends.ModelBackend'
        auth_login(request, user_account)

        result['success'] = True
        return render(request, 'registration/activation_confirm.html', result)

    except Exception, e:
        print "Error action confirm_activation : %s" % e
        raise Exception(
            "ERROR : Internal Server Error .Please contact administrator.")


@login_required(login_url='/login/')
def profile(request): 
    try:
        user = request.user
        form_profile = ProfileForm(user=user)
        context = {'full_name': user.full_name, 'email': user.email, 'gender': user.gender,
            'phone': user.phone, 'birth_date': user.birth_date, 'address': user.address, 
            'form': form_profile, 'is_profile': True
        }
 
        if request.method == 'POST':
            print request.POST['birth_date']
            form_profile = ProfileForm(request.POST, user=user)
            if(form_profile.is_valid()):
                form_profile.save()
                messages.success(request, _(
                    'Update profile Successfully.'))
                return redirect(reverse('profile'))

            else:
                context['full_name'] = request.POST[
                    'full_name'] if 'full_name' in request.POST else None
                context['email'] = request.POST[
                    'email'] if 'email' in request.POST else None
                context['gender'] = request.POST[
                    'gender'] if 'gender' in request.POST else None
                context['phone'] = request.POST[
                    'phone'] if 'phone' in request.POST else None
                context['birth_date'] = request.POST[
                    'birth_date'] if 'birth_date' in request.POST else None
                context['address'] = request.POST[
                    'address'] if 'address' in request.POST else None
                context['form'] = form_profile

        return render(request, 'registration/profile.html', context)
    except Exception, e:
        print "Error Home: ", e
        raise Exception(
            "ERROR : Internal Server Error .Please contact administrator.")


@login_required(login_url='/login/')
def change_password(request):
    try:
        user = request.user
        form = ChangePasswordForm(user=user)

        context = {'form': form, 'is_change_password': True}

        if request.method == 'POST':
            form = ChangePasswordForm(request.POST, user=user)
            context['form'] = form
            if form.is_valid():
                form.save()
                print request.user.is_authenticated()
                messages.success(request, _('Update Password Successfully.'))
                return redirect(reverse('change_password'))

        return render(request, 'registration/change_password.html', context)
    except Exception, e:
        print "error", e
        raise Exception(
            "ERROR : Internal Server Error .Please contact administrator.")