# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20160804_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='name_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Nombre'),
        ),
        migrations.AddField(
            model_name='content',
            name='name_es',
            field=models.CharField(max_length=200, null=True, verbose_name='Nombre'),
        ),
        migrations.AddField(
            model_name='content',
            name='text_en',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='content',
            name='text_es',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='content',
            name='title_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Title'),
        ),
        migrations.AddField(
            model_name='content',
            name='title_es',
            field=models.CharField(max_length=200, null=True, verbose_name='Title'),
        ),
    ]
