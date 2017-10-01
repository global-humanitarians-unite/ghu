# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-01 14:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ghu_main', '0004_toolkits'),
    ]

    operations = [
        migrations.AddField(
            model_name='navbarentry',
            name='url',
            field=models.CharField(blank=True, choices=[('ghu_main:toolkits', 'Toolkits listing')], max_length=256, verbose_name='Special page'),
        ),
        migrations.AlterField(
            model_name='navbarentry',
            name='page',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ghu_main.Page'),
        ),
    ]