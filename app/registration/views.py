# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import logout as auth_logout, login as auth_login
from forms import *

# Create your views here.
def login(request): 
    try:
        if request.user.is_authenticated():
            return redirect(reverse('home'))
        else:
            result = {}
            if request.method == 'POST':
                login_form = LoginForm(request.POST, request=request)
                if login_form.is_valid():
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


def register(request): 
    try:
        return render(request, 'registration/register.html')
    except Exception, e:
        print "Error Home: ", e
        raise Exception(
            "ERROR : Internal Server Error .Please contact administrator.")


def profile(request): 
    try:
        return render(request, 'registration/profile.html')
    except Exception, e:
        print "Error Home: ", e
        raise Exception(
            "ERROR : Internal Server Error .Please contact administrator.")