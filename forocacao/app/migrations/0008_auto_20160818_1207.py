# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_remove_organization_email'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='attendee',
            options={'ordering': ['first_name', 'last_name'], 'verbose_name': 'Asistente', 'verbose_name_plural': 'Asistentes'},
        ),
        migrations.AlterField(
            model_name='attendeepayment',
            name='attendee',
            field=models.ForeignKey(related_name='payments', verbose_name='Asistente', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='attendeereceipt',
            name='attendee',
            field=models.OneToOneField(related_name='receipt', verbose_name='Asistente', to='app.Attendee'),
        ),
        migrations.AlterField(
            model_name='organization',
            name='type',
            field=models.CharField(blank=True, max_length=1, null=True, choices=[('O', 'Organizador'), ('E', 'Exhibidor'), ('S', 'Speaker')]),
        ),
    ]
