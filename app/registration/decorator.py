from django.shortcuts import redirect
from django.core.urlresolvers import reverse


def is_authenticated(f):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse('home'))
        return f(request, *args, **kwargs)
    return wrapper