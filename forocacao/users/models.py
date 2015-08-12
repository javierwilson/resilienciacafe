# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.contrib.auth.models import AbstractUser
from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from filer.fields.image import FilerImageField
from django_countries.fields import CountryField

from forocacao.app.models import Conference, Profession, AttendeeType, Activity


@python_2_unicode_compatible
class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    name = models.CharField(_("Name of User"), blank=True, max_length=255)

    conference = models.ForeignKey(Conference, null=True)
    profession = models.ForeignKey(Profession, null=True)
    phone = models.CharField(max_length=50, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    country = CountryField(null=True, blank=True)
    document = models.CharField(max_length=50, null=True, blank=True)
    attendee_type = models.ForeignKey(AttendeeType, null=True)
    photo = models.ImageField(null=True, blank=True)
    text = models.TextField(blank=True,
                                 verbose_name=_('Biography'),
                                 help_text='Try and enter few some more lines')
    activities = models.ManyToManyField(Activity)

    class Meta:
        verbose_name = _("Attendee")
        verbose_name_plural = _("Attendees")

    def __str__(self):
        return self.name
        #return "%s %s" % (self.user.first_name, self.user.last_name)

    def get_absolute_url(self):
        return reverse('users:detail', kwargs={'username': self.username})

