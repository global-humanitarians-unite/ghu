# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-09-30 18:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ghu_main', '0002_page-templates'),
    ]

    operations = [
        migrations.CreateModel(
            name='NavbarEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveIntegerField(db_index=True, editable=False)),
                ('label', models.CharField(max_length=256)),
                ('page', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ghu_main.Page')),
            ],
            options={
                'ordering': ('order',),
                'abstract': False,
            },
        ),
    ]
