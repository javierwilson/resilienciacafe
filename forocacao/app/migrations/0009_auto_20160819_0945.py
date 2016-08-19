# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20160818_1207'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='text_en',
            field=models.TextField(null=True, verbose_name='Descripci\xf3n', blank=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='text_es',
            field=models.TextField(null=True, verbose_name='Descripci\xf3n', blank=True),
        ),
    ]
