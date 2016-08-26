# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20160819_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='place',
            field=models.CharField(max_length=300, null=True, verbose_name='Lugar', blank=True),
        ),
    ]
