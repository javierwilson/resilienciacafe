# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20160805_1435'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='translation',
            field=models.BooleanField(default=False, verbose_name='The forum will be held in Spanish.  Will you need translation to English?'),
        ),
    ]
