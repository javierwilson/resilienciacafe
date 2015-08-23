# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from filer.fields.image import FilerImageField
from django_countries.fields import CountryField
from model_utils import Choices
from colorfield.fields import ColorField

from forocacao.users.models import User

class Event(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Title'))
    slug = models.SlugField()
    STATUS = Choices(('inactive',_('inactive')), ('draft', _('draft')), ('published', _('published')), ('frontpage',_('frontpage')))
    status = models.CharField(choices=STATUS, default=STATUS.draft, max_length=20, verbose_name=_('Status'))
    activities = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Activities'))
    text = models.TextField(blank=True,
                                 verbose_name=_('Event description'),
                                 help_text='Try and enter few some more lines')
    logo = FilerImageField(blank=True, null=True, related_name='event_logos', verbose_name=_('Logo'))
    image = FilerImageField(blank=True, null=True, related_name='event_images', verbose_name=_('Image'))
    image_footer = FilerImageField(blank=True, null=True, related_name='event_footers', verbose_name=_('Image footer') )
    start = models.DateField(blank=True, null=True, verbose_name=_('Start'))
    end = models.DateField(blank=True, null=True, verbose_name=_('End'))
    types = models.ManyToManyField('AttendeeType', through='AttendeeTypeEvent')
    professions = models.ManyToManyField('Profession')
    payment_methods = models.ManyToManyField('PaymentMethod')
    badge_size_x = models.IntegerField(null=True, blank=True)
    badge_size_y = models.IntegerField(null=True, blank=True)
    badge_color = ColorField(default='ffffff')

    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __unicode__(self):
        return self.name

class Activity(models.Model):
    event = models.ForeignKey('Event', verbose_name=_('Event'))
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    slug = models.SlugField()
    organizer = models.ForeignKey('users.User', null=True, verbose_name=_('Organizer'))
    text = models.TextField(blank=True,
                                 verbose_name=_('Activity description'),
                                 help_text='Try and enter few some more lines')
    image = FilerImageField(blank=True, null=True, related_name='activity_images', verbose_name=_('Image'))
    image_footer = FilerImageField(blank=True, null=True, related_name='activity_footers', verbose_name=_('Image footer'))
    start = models.DateTimeField(blank=True, null=True, verbose_name=_('Start'))
    end = models.DateTimeField(blank=True, null=True, verbose_name=_('End'))

    class Meta:
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")

    def __unicode__(self):
        return self.name

class Profession(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    slug = models.SlugField()
    text = models.TextField(blank=True,
                                 verbose_name=_('Profession description'),
                                 help_text='Try and enter few some more lines')

    class Meta:
        verbose_name = _("Profession")
        verbose_name_plural = _("Professions")

    def __unicode__(self):
        return self.name

class PaymentMethod(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))

    class Meta:
        verbose_name = _("Payment Method")
        verbose_name_plural = _("Payment Methods")

    def __unicode__(self):
        return self.name

class AttendeeTypeEvent(models.Model):
    attendeetype = models.ForeignKey('AttendeeType')
    event = models.ForeignKey('Event')
    price = models.DecimalField(max_digits=8, decimal_places=2,)
    eb_price = models.DecimalField(max_digits=8, decimal_places=2,)

    class Meta:
        verbose_name = _("Attendee Type in Event")
        verbose_name_plural = _("Attendee Types in Events")

class AttendeeType(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))

    class Meta:
        verbose_name = _("Attendee Type")
        verbose_name_plural = _("Attendee Types")

    def __unicode__(self):
        return self.name

class AttendeePayment(models.Model):
    attendee = models.ForeignKey('users.User', verbose_name=_('Attendee'))
    payment_method = models.ForeignKey('PaymentMethod', verbose_name=_('Payment Method'))
    date = models.DateField(verbose_name=_("Date"))
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    reference = models.CharField(max_length=20)
    note = models.CharField(max_length=200)

    class Meta:
        verbose_name = _("Attendee Payment")
        verbose_name_plural = _("Attendee Payments")

class Font(models.Model):
    name = models.CharField(max_length=50, unique=True)
    filename = models.CharField(max_length=250, unique=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name

class EventBadge(models.Model):
    event = models.ForeignKey('Event', verbose_name=_('Event'))
    FIELDS = (('event',_('Event')), ('name', _('Complete name')), ('first_name', _('First name')), ('last_name', _('Last name')),
            ('profession',_('Profession')), ('country',_('Country')), ('type',_('Type')), ('email',_('E-mail')), ('text', _('Text')),
            ('logo',_('Logo')), ('photo',_('Photo')))
    field = models.CharField(max_length=50, choices=FIELDS)
    color = ColorField(default='', null=True, blank=True)
    font = models.ForeignKey('Font', null=True, blank=True)
    size = models.IntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    format = models.CharField(max_length=50, null=True, blank=True)

    def __unicode__(self):
        return self.field

class Attendee(User):
    class Meta:
        verbose_name = _("Attendee")
        verbose_name_plural = _("Attendees")
        proxy = True

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
