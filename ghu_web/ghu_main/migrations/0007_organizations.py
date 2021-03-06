# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-10-24 13:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('ghu_main', '0007_orgprofiletemplate'), ('ghu_main', '0008_orgprofile'), ('ghu_main', '0009_delete_orgprofiletemplate'), ('ghu_main', '0010_auto_20171018_2201'), ('ghu_main', '0011_auto_20171018_2203'), ('ghu_main', '0012_remove_orgprofile_location'), ('ghu_main', '0013_orgprofile_location'), ('ghu_main', '0014_orgprofile_summary'), ('ghu_main', '0015_auto_20171018_2210')]

    dependencies = [
        ('ghu_main', '0006_toolkit_rewework'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrgProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('name', models.CharField(max_length=256)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=256)),
                ('description', models.TextField()),
                ('location', models.CharField(max_length=256, null=True)),
                ('summary', models.CharField(max_length=256, null=True)),
            ],
        ),
    ]
