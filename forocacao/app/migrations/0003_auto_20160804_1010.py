# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20160729_1034'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='organization',
            options={'ordering': ['name']},
        ),
        migrations.RemoveField(
            model_name='organization',
            name='email',
        ),
        migrations.AddField(
            model_name='organization',
            name='event',
            field=models.ForeignKey(default=1, verbose_name='Event', to='app.Event'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='organization',
            name='photo',
            field=models.ImageField(upload_to=b'', null=True, verbose_name='Photo', blank=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='text',
            field=models.TextField(verbose_name='Description', blank=True),
        ),
        migrations.AddField(
            model_name='organization',
            name='type',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[('O', 'Organizador'), ('E', 'Exhibidor')]),
        ),
        migrations.AddField(
            model_name='organization',
            name='url',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='payment_methods',
            field=models.ManyToManyField(to='app.PaymentMethod', verbose_name='Payment Methods', blank=True),
        ),
        migrations.AlterField(
            model_name='event',
            name='professions',
            field=models.ManyToManyField(to='app.Profession', verbose_name='Proffesions', blank=True),
        ),
        migrations.AlterField(
            model_name='organization',
            name='name',
            field=models.CharField(max_length=50, null=True, verbose_name='Nombre', blank=True),
        ),
    ]
