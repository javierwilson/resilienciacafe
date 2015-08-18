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

class Conference(models.Model):
    name = models.CharField(max_length=200)
    title = models.CharField(max_length=200, null=True, blank=True)
    slug = models.SlugField()
    STATUS = Choices(('inactive',_('inactive')), ('draft', _('draft')), ('published', _('published')), ('frontpage',_('frontpage')))
    status = models.CharField(choices=STATUS, default=STATUS.draft, max_length=20)
    activities = models.CharField(max_length=50, null=True, blank=True)
    text = models.TextField(blank=True,
                                 verbose_name=_('Conference description'),
                                 help_text='Try and enter few some more lines')
    logo = FilerImageField(blank=True, null=True, related_name='conference_logos')
    image = FilerImageField(blank=True, null=True, related_name='conference_images')
    image_footer = FilerImageField(blank=True, null=True, related_name='conference_footers')
    start = models.DateField(blank=True, null=True)
    end = models.DateField(blank=True, null=True)

    class Meta:
        verbose_name = _("Concerence")
        verbose_name_plural = _("Conferences")

    def __unicode__(self):
        return self.name

class Activity(models.Model):
    conference = models.ForeignKey(Conference)
    name = models.CharField(max_length=200)
    slug = models.SlugField()
    organizer = models.ForeignKey('users.User', null=True)
    text = models.TextField(blank=True,
                                 verbose_name=_('Activity description'),
                                 help_text='Try and enter few some more lines')
    image = FilerImageField(blank=True, null=True, related_name='activity_images')
    image_footer = FilerImageField(blank=True, null=True, related_name='activity_footers')
    start = models.DateTimeField(blank=True, null=True)
    end = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name = _("Activity")
        verbose_name_plural = _("Activities")

    def __unicode__(self):
        return self.name

class Profession(models.Model):
    conference = models.ForeignKey(Conference)
    name = models.CharField(max_length=200)
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
        proxy = True

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)
