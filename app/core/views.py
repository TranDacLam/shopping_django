# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from models import *
from datetime import *

# Create your views here.
def home(request):
    try:
        data_slide = SlideShow.objects.filter(is_draft=False)
        hot_products = Product.objects.filter(hot=True)
        new_products = Product.objects.filter(is_draft=False).order_by('modified')[:4]
        promotion_products  = Product.objects.filter(is_draft=False, promotion__isnull=False).order_by('modified')[:4]

        return render(request, 'websites/home.html', {
                'data_slide': data_slide, 'hot_products': hot_products,
                'new_products': new_products, 'promotion_products': promotion_products
            })
    except Exception, e:
        print "Error Home: ", e
        raise Exception(
            "ERROR : Internal Server Error .Please contact administrator.")


def products(request):
    try:
        title = _("HELLO")
        return render(request, 'websites/products.html', {'title': title})
    except Exception, e:
        print "Error Home: ", e
        raise Exception(
            "ERROR : Internal Server Error .Please contact administrator.")


def product_detail(request, id):
    try:
        title = _("HELLO")
        return render(request, 'websites/product_detail.html', {'title': title})
    except Exception, e:
        print "Error Home: ", e
        raise Exception(
            "ERROR : Internal Server Error .Please contact administrator.")


def cart(request):
    try:
        title = _("HELLO")
        return render(request, 'websites/cart.html', {'title': title})
    except Exception, e:
        print "Error Home: ", e
        raise Exception(
            "ERROR : Internal Server Error .Please contact administrator.")


def contact(request):
    try:
        title = _("HELLO")
        return render(request, 'websites/contact.html', {'title': title})
    except Exception, e:
        print "Error Home: ", e
        raise Exception(
            "ERROR : Internal Server Error .Please contact administrator.")


def about(request):
    try:
        title = _("HELLO")
        return render(request, 'websites/about.html', {'title': title})
    except Exception, e:
        print "Error Home: ", e
        raise Exception(
            "ERROR : Internal Server Error .Please contact administrator.")