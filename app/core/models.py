# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db import models
from core.custom_models import *
import datetime

# Create your models here.
class DateTimeModel(models.Model):
    """
    Abstract model that is used for the model using created and modified fields
    """
    created = models.DateTimeField(_('Created Date'), auto_now_add=True,
                                   editable=False)
    modified = models.DateTimeField(
        _('Modified Date'), auto_now=True, editable=False)

    def __init__(self, *args, **kwargs):
        super(DateTimeModel, self).__init__(*args, **kwargs)

    class Meta:
        abstract = True


class SlideShow(DateTimeModel):
    image = models.ImageField(
        _("Image"), max_length=255, upload_to="slide")
    sub_url = models.CharField(_("Sub Url"), max_length=1000)
    is_draft = models.BooleanField(default=False)

    def __str__(self):
        return '%s' % (self.image)

    class Meta:
        verbose_name = _('Slide Show')


class Category(models.Model):
    name = models.CharField(_('Name'), max_length=100, unique=True)
    slug = models.SlugField(_('Slug'), max_length=100)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Product(DateTimeModel):
    name = models.CharField(_("Product Name"), max_length=255)
    slug = models.SlugField(_("Slug"), max_length=255)
    image = models.ImageField(
        _('Product'), max_length=255, upload_to="product")
    avg_rate = models.IntegerField(_('Avg Rate'), editable=True, default=0)
    unit_price = models.FloatField(_('Unit price'), blank=False)
    promotion = models.FloatField(_('Promotion'), null=True, blank=True)
    inventory = models.IntegerField(_('Inventory'), null=True, blank=True)
    description = models.TextField(_("Description"))
    hot = models.BooleanField(default=False)
    is_draft = models.BooleanField(default=False)
    category = models.ForeignKey('Category', related_name='category_product_rel',
                                 on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name = _('Product')
        verbose_name_plural = _('Products')


class Rate(DateTimeModel):
    # using name as key mapping genre 18, populate ..etc
    point = models.IntegerField(_('Point'))
    user = models.ForeignKey('User', related_name='user_rate_rel',
                                 on_delete=models.CASCADE)
    product = models.ForeignKey('Product', related_name='product_rate_rel',
                                 on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.point)

    class Meta:
        verbose_name = _('Rate')


class Bill(DateTimeModel):
    TYPE_STATUS = (
        ('pending', 'Pending'),
        ('accept', 'Accept'),
        ('delivered', 'Delivered'),
        ('reject', 'Reject'),
        ('cancel', 'Cancel'),
    )

    order_date = models.DateField(_("Order Date"), default=datetime.date.today, editable=True)
    status = models.CharField(_("Status"), max_length=50, choices=TYPE_STATUS)
    note = models.TextField(_("Note"), null=True, blank=True)
    total = models.FloatField(_('Total'), null=True, blank=True, editable=True)
    user = models.ForeignKey('User', related_name='user_bill_rel',
                                 on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.order_date)

    class Meta:
        verbose_name = _('Bill')
        verbose_name_plural = _('Bills')


class BillDetail(DateTimeModel):
    quantity = models.FloatField(_('Total'), null=True, blank=True)
    unit_price = models.FloatField(_('Unit price'), null=True, blank=True)
    product = models.ForeignKey('Product', related_name='product_bill_detail_rel',
                                 on_delete=models.CASCADE)
    bill = models.ForeignKey('Bill', related_name='bill_detail_rel',
                                 on_delete=models.CASCADE)

    def __str__(self):
        return '%s' % (self.name)

    class Meta:
        verbose_name = _('Bill Detail')
        verbose_name_plural = _('Bill Detail')


class Comment(DateTimeModel):
    content = models.TextField(_("Content"))
    parent = models.IntegerField(_('Parent'), null=True, blank=True)
    product = models.ForeignKey('Product', related_name='product_comment_rel',
                                 on_delete=models.CASCADE)
    user = models.ForeignKey('User', related_name='user_comment_rel',
                                 on_delete=models.CASCADE)
    def __str__(self):
        return '%s' % (self.full_name)

    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')


class Contact(DateTimeModel):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=50)
    phone = models.CharField(max_length=20, null=True, blank=True)
    subject = models.CharField(max_length=50, null=True, blank=True)
    message = models.TextField()

    def __str__(self):
        return '%s' % (self.name)
