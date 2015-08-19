# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from filer.fields.image import FilerImageField
from django_countries.fields import CountryField
from model_utils import Choices
from smart_selects.db_fields import ChainedForeignKey


@python_2_unicode_compatible
class User(AbstractUser):

    name = models.CharField(_("Name of User"), blank=True, max_length=255)

    event = models.ForeignKey('app.Event', null=True, verbose_name=_('Event'))
    profession = models.ForeignKey('app.Profession', null=True, blank=True, verbose_name=_('Profession'))
    phone = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Phone'))
    age = models.IntegerField(null=True, blank=True, verbose_name=_('Age'))
    country = CountryField(null=True, blank=True, verbose_name=_('Country'))
    document = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Document'))
    TYPE = Choices(('regular',_('Regular')), ('speaker', _('Speaker')), ('sponsor', _('Sponsor')), ('organizer',_('Oganizer')), ('special',_('Special')))
    type = models.CharField(choices=TYPE, default=TYPE.regular, max_length=20, verbose_name=_('Type'))
    photo = models.ImageField(null=True, blank=True, verbose_name=_('Photo'))
    text = models.TextField(blank=True,
                                 verbose_name=_('Biography'),
                                 help_text='Try and enter few some more lines')
    activities = models.ManyToManyField('app.Activity', blank=True, verbose_name=_('Activity'))

    class Meta:
        verbose_name = _("Attendee")
        verbose_name_plural = _("Attendees")
        permissions = (
            ("can_approve_participant", "Can approve participant"),
        )

    def __str__(self):
        return self.name
        #return "%s %s" % (self.user.first_name, self.user.last_name)

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})
