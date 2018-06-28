# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _

# Create your views here.
def home(request):
    try:
        title = _("HELLO")
        return render(request, 'websites/home.html', {'title': title})
    except Exception, e:
        print "Error Home: ", e
        raise Exception(
            "ERROR : Internal Server Error .Please contact administrator.")