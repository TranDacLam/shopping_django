# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-30 02:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
