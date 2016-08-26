# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_auto_20160819_0945'),
    ]

    operations = [
        migrations.AddField(
            model_name='organization',
            name='title',
            field=models.CharField(max_length=300, null=True, verbose_name='T\xedtulo', blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(max_length=200, null=True, verbose_name='Nombre', blank=True),
        ),
    ]
