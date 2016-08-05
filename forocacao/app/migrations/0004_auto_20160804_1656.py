# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20160804_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='name_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Event'),
        ),
        migrations.AddField(
            model_name='event',
            name='name_es',
            field=models.CharField(max_length=200, null=True, verbose_name='Event'),
        ),
        migrations.AddField(
            model_name='event',
            name='title_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Title', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='title_es',
            field=models.CharField(max_length=200, null=True, verbose_name='Title', blank=True),
        ),
    ]
