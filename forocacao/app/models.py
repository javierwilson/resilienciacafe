# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from filer.fields.image import FilerImageField
from django_countries.fields import CountryField
from model_utils import Choices

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
    event = models.ForeignKey('Event', verbose_name=_('Event'))
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

class Attendee(User):
    class Meta:
        verbose_name = _("Attendee")
        verbose_name_plural = _("Attendees")
        proxy = True

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
