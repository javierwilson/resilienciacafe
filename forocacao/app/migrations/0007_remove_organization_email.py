# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20160805_1203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organization',
            name='email',
        ),
    ]
