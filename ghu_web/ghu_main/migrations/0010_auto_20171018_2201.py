# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-19 02:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ghu_main', '0009_delete_orgprofiletemplate'),
    ]

    operations = [
        migrations.AddField(
            model_name='orgprofile',
            name='location',
            field=models.CharField(default='DEFAULT VALUE', max_length=256),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='orgprofile',
            name='email',
            field=models.EmailField(max_length=254),
        ),
    ]
