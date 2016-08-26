# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0010_auto_20160819_1056'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='title_en',
            field=models.CharField(max_length=300, null=True, verbose_name='T\xedtulo', blank=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='title_es',
            field=models.CharField(max_length=300, null=True, verbose_name='T\xedtulo', blank=True),
        ),
    ]
