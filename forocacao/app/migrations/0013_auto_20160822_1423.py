# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_organization_place'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='place_en',
            field=models.CharField(max_length=300, null=True, verbose_name='Lugar', blank=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='place_es',
            field=models.CharField(max_length=300, null=True, verbose_name='Lugar', blank=True),
        ),
    ]
