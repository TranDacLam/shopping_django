# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse, Http404
from django.utils.translation import ugettext_lazy as _
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Avg
import json
from models import *
from datetime import *
from cart import *

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
        category_id = request.GET.get('category', None)
        sort = request.GET.get('sort', None)

        categories = Category.objects.all()

        if  category_id:
            product_list = Product.objects.filter(is_draft=False, category=category_id).order_by('modified')
        elif sort == 'hot':
            product_list = Product.objects.filter(is_draft=False, hot=True).order_by('modified')
        elif sort == 'promotion':
            product_list = Product.objects.filter(is_draft=False, promotion__isnull=False).order_by('modified')
        else:
            product_list = Product.objects.filter(is_draft=False).order_by('modified')

        paginator = Paginator(product_list, 9)
        page = request.GET.get('page', 1)

        try:
            products = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            products = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            products = paginator.page(paginator.num_pages)

        return render(request, 'websites/products.html', {'categories': categories, 'products': products, 'sort': sort})
    except Exception, e:
        print "Error products: ", e
        raise Exception(
            "ERROR : Internal Server Error .Please contact administrator.")


def product_detail(request, id):
    try:
        product = Product.objects.get(pk=id)
        related_products = Product.objects.filter(category=product.category.id).order_by('modified')[:4]

        return render(request, 'websites/product_detail.html', {'product': product, 'related_products':related_products})
    
    except Product.DoesNotExist, e:
        print "Error product_detail : %s" % e
        raise Http404()

    except Exception, e:
        print "Error product_detail: ", e
        raise Exception(
            "ERROR : Internal Server Error .Please contact administrator.")


def product_rating(request):
    try:
        if request.user.is_authenticated():
            point = request.POST.get('point')
            product_id = request.POST.get('product_id')
            product = Product.objects.get(pk=product_id)
            user = request.user

            rate_exist = Rate.objects.filter(user_id=user.id, product_id=product_id)
            if rate_exist:
                rate = Rate.objects.get(pk=rate_exist)
                rate.point = point
            else:
                rate = Rate(point=point, product_id=product_id, user_id=user.id)

            rate.save()

            avg_point = rate_exist.aggregate(Avg('point'))

            product.avg_rate = avg_point['point__avg']
            product.save()

            return JsonResponse({"message": _("Thank you for rating"), "point": avg_point['point__avg']}, status=200)

        return JsonResponse({"message": _("Please log in to rate.")}, status=403)

    except Product.DoesNotExist, e:
        print "Error product_rating : %s" % e
        raise Http404()

    except Exception, e:
        print "Error product_rating: ", e
        raise Exception(
            "ERROR : Internal Server Error .Please contact administrator.")


def cart(request):
    try:

        return render(request, 'websites/cart.html')
    except Exception, e:
        print "Error cart: ", e
        raise Exception(
            "ERROR : Internal Server Error .Please contact administrator.")



def add_to_cart(request):
    try:
        path_url = request.POST.get('path_url', None)
        product_id = request.POST.get('product_id', None)
        quantity = request.POST.get('quantity', None)


        product = Product.objects.get(id=int(product_id))

        if 'CART' in request.session:
            cart = Cart(request.session['CART'])
        else:
            cart = Cart({})

        cart.add(product, int(quantity))

        request.session['CART'] = {
            'total_price': cart.total_price,
            'total_quantity': cart.total_quantity,
            'items': cart.items
        }

        print request.session['CART']

        if 'add_to_cart' in request.POST:
            return redirect(reverse('home'))
        elif 'buy_now' in request.POST:

            return redirect(reverse('cart'))

        # return redirect(reverse(path_url))
            
    except Product.DoesNotExist, e:
        print "Error Cart : %s" % e
        raise Http404()

    except Exception, e:
        print "Error Cart: ", e
        raise Exception(
            "ERROR : Internal Server Error .Please contact administrator.")


def contact(request):
    try:
        return render(request, 'websites/contact.html')
    except Exception, e:
        print "Error contact: ", e
        raise Exception(
            "ERROR : Internal Server Error .Please contact administrator.")


def about(request):
    try:
        return render(request, 'websites/about.html')
    except Exception, e:
        print "Error about: ", e
        raise Exception(
            "ERROR : Internal Server Error .Please contact administrator.")


def checkout(request):
    try:
        return render(request, 'websites/about.html')
    except Exception, e:
        print "Error checkout: ", e
        raise Exception(
            "ERROR : Internal Server Error .Please contact administrator.")