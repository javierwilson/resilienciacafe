# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='emergency_name',
            field=models.CharField(default='', max_length=30, verbose_name='Emergency Contact Name'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='emergency_phone',
            field=models.CharField(default='', max_length=30, verbose_name='Emergency Contact Telephone'),
            preserve_default=False,
        ),
    ]
