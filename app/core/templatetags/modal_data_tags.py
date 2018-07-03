# -*- coding: utf-8 -*-
from django import template
from django.utils.safestring import mark_safe
from django.contrib.humanize.templatetags.humanize import intcomma
register = template.Library()

@register.filter
def rating_product(value):
    result = ''
    for i in range(0, 5):
        if i < value:
            result += '<i class="fa fa-star star-full"></i>'
        else:
            result += '<i class="fa fa-star"></i>'
            
    return mark_safe(result)


@register.filter
def currency(value):
    value = '{:,}'.format(value)
    return value
    