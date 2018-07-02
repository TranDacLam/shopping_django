# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from models import *
from django import forms
import custom_models

# Register your models here.

class ReadOnlyAdmin(admin.ModelAdmin):
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]


    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class SlideShowAdmin(admin.ModelAdmin):
    pass
admin.site.register(SlideShow, SlideShowAdmin)


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    pass
admin.site.register(Category, CategoryAdmin)


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    pass
admin.site.register(Product, ProductAdmin)


class CommentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Comment, CommentAdmin)


class ContactAdmin(ReadOnlyAdmin):
    pass
admin.site.register(Contact, ContactAdmin)


class BillDetailAdmin(admin.StackedInline):
    model = BillDetail 


class BillAdmin(admin.ModelAdmin):
    inlines = [BillDetailAdmin]
    pass
admin.site.register(Bill, BillAdmin)