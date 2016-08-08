# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models
import filer.fields.image
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
        ('filer', '0001_initial'),
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendee',
            fields=[
            ],
            options={
                'ordering': ['first_name', 'last_name'],
                'verbose_name': 'Attendee',
                'proxy': True,
                'verbose_name_plural': 'Attendees',
            },
            bases=('users.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='news',
            name='event',
            field=models.ForeignKey(related_name='news', verbose_name='Event', to='app.Event'),
        ),
        migrations.AddField(
            model_name='logo',
            name='event',
            field=models.ForeignKey(related_name='logos', verbose_name='Event', to='app.Event'),
        ),
        migrations.AddField(
            model_name='logo',
            name='image',
            field=filer.fields.image.FilerImageField(verbose_name='Logo', to='filer.Image'),
        ),
        migrations.AddField(
            model_name='field',
            name='event',
            field=models.ForeignKey(related_name='fields', verbose_name='Event', to='app.Event'),
        ),
        migrations.AddField(
            model_name='eventbadge',
            name='event',
            field=models.ForeignKey(verbose_name='Event', to='app.Event'),
        ),
        migrations.AddField(
            model_name='eventbadge',
            name='font',
            field=models.ForeignKey(verbose_name='Font', blank=True, to='app.Font', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='activities',
            field=models.ManyToManyField(to='app.Activity', verbose_name='Activities', blank=True),
        ),
        migrations.AddField(
            model_name='event',
            name='image',
            field=filer.fields.image.FilerImageField(related_name='event_images', verbose_name='Imagen', blank=True, to='filer.Image', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='image_footer',
            field=filer.fields.image.FilerImageField(related_name='event_footers', verbose_name='Image footer', blank=True, to='filer.Image', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='logo',
            field=filer.fields.image.FilerImageField(related_name='event_logos', verbose_name='Logo', blank=True, to='filer.Image', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='payment_methods',
            field=models.ManyToManyField(to='app.PaymentMethod', verbose_name='Payment Methods'),
        ),
        migrations.AddField(
            model_name='event',
            name='pdflogo',
            field=filer.fields.image.FilerImageField(related_name='event_pdflogos', verbose_name='PDF Logo', blank=True, to='filer.Image', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='professions',
            field=models.ManyToManyField(to='app.Profession', verbose_name='Proffesions'),
        ),
        migrations.AddField(
            model_name='event',
            name='translucid',
            field=filer.fields.image.FilerImageField(related_name='translucid_images', verbose_name='Translucid Image', blank=True, to='filer.Image', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='types',
            field=models.ManyToManyField(to='app.AttendeeType', through='app.AttendeeTypeEvent'),
        ),
        migrations.AddField(
            model_name='content',
            name='event',
            field=models.ForeignKey(related_name='contents', verbose_name='Event', to='app.Event'),
        ),
        migrations.AddField(
            model_name='content',
            name='image',
            field=filer.fields.image.FilerImageField(verbose_name='Imagen', blank=True, to='filer.Image', null=True),
        ),
        migrations.AddField(
            model_name='attendeetypeevent',
            name='attendeetype',
            field=models.ForeignKey(verbose_name='Attendee Type', to='app.AttendeeType'),
        ),
        migrations.AddField(
            model_name='attendeetypeevent',
            name='event',
            field=models.ForeignKey(verbose_name='Event', to='app.Event'),
        ),
        migrations.AddField(
            model_name='attendeereceipt',
            name='attendee',
            field=models.OneToOneField(related_name='receipt', verbose_name='Attendee', to='app.Attendee'),
        ),
        migrations.AddField(
            model_name='attendeepayment',
            name='attendee',
            field=models.ForeignKey(related_name='payments', verbose_name='Attendee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attendeepayment',
            name='payment_method',
            field=models.ForeignKey(verbose_name='Payment Method', to='app.PaymentMethod'),
        ),
        migrations.AddField(
            model_name='activity',
            name='image',
            field=filer.fields.image.FilerImageField(related_name='activity_images', verbose_name='Imagen', blank=True, to='filer.Image', null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='image_footer',
            field=filer.fields.image.FilerImageField(related_name='activity_footers', verbose_name='Image footer', blank=True, to='filer.Image', null=True),
        ),
        migrations.AddField(
            model_name='activity',
            name='organizer',
            field=models.ForeignKey(verbose_name='Organizer', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
