# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_user_translation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='translation',
            field=models.BooleanField(default=False, verbose_name='Needs translation'),
        ),
    ]
