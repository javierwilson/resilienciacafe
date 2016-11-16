# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import embed_video.fields


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_auto_20160822_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='video',
            field=embed_video.fields.EmbedVideoField(null=True, blank=True),
        ),
    ]
