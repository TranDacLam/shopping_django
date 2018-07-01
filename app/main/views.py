# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
def custom_404(request):
	return render(request, 'errors/404.html', {}, status=404)

def custom_500(request):
	return render(request, 'errors/500.html', {}, status=500)