# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from django.db import models
from django.db.models import Sum, Max
from django.conf import settings
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _

from filer.fields.image import FilerImageField
from django_countries.fields import CountryField
from model_utils import Choices
from model_utils.fields import StatusField
from colorfield.fields import ColorField

from forocacao.users.models import User

class News(models.Model):
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    media = models.CharField(max_length=200, verbose_name=_('Media'))
    url = models.URLField()
    date = models.DateField()
    event = models.ForeignKey('Event', related_name='news', verbose_name=_('Event'))

    class Meta:
        ordering = ['-date', 'title']

    def __unicode__(self):
        return self.title

class Invited(models.Model):
    first_name = models.CharField(max_length=200, verbose_name=_('First name'))
    last_name = models.CharField(max_length=200, verbose_name=_('Last name'))
    organization = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Organization'))
    email = models.CharField(max_length=100, verbose_name=_('E-Mail'), unique=True)

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = _("Invited")
        verbose_name_plural = _("Invited")

    def registered(self):
        test = Attendee.objects.filter(email=self.email)
        if test:
            return True
        else:
            return False
    registered.short_description = _("Registered")
    registered.boolean = True

    def __unicode__(self):
        return self.email



class Event(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Event'))
    title = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Title'))
    organizer = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Organizer'))
    slug = models.SlugField()
    STATUS = Choices(('inactive',_('inactive')), ('draft', _('draft')), ('published', _('published')), ('frontpage',_('frontpage')))
    status = models.CharField(choices=STATUS, default=STATUS.draft, max_length=20, verbose_name=_('Status'))
    activities_label = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Activities label'))
    activities = models.ManyToManyField('Activity', blank=True, verbose_name=_('Activities'))
    text = models.TextField(blank=True,
                                 verbose_name=_('Event description'),
                                 help_text='Try and enter few some more lines')
    logo = FilerImageField(blank=True, null=True, related_name='event_logos', verbose_name=_('Logo'))
    pdflogo = FilerImageField(blank=True, null=True, related_name='event_pdflogos', verbose_name=_('PDF Logo'))
    pdfnote = models.TextField(blank=True, null=True, verbose_name=_('PDF and Approval Note'))
    reject_note = models.TextField(blank=True, null=True, verbose_name=_('Reject Note'))
    image = FilerImageField(blank=True, null=True, related_name='event_images', verbose_name=_('Image'))
    translucid = FilerImageField(blank=True, null=True, related_name='translucid_images', verbose_name=_('Translucid Image'))
    image_footer = FilerImageField(blank=True, null=True, related_name='event_footers', verbose_name=_('Image footer') )
    eb_start = models.DateField(blank=True, null=True, verbose_name=_('Early Bird Start'))
    eb_end = models.DateField(blank=True, null=True, verbose_name=_('Early Bird End'))
    start = models.DateTimeField(blank=True, null=True, verbose_name=_('Start'))
    end = models.DateTimeField(blank=True, null=True, verbose_name=_('End'))
    place = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Place'))
    types = models.ManyToManyField('AttendeeType', through='AttendeeTypeEvent')
    professions = models.ManyToManyField('Profession', verbose_name=_('Proffesions'), blank=True)
    payment_methods = models.ManyToManyField('PaymentMethod', verbose_name=_('Payment Methods'), blank=True)
    badge_size_x = models.IntegerField(null=True, blank=True, verbose_name=_('Badge size X'))
    badge_size_y = models.IntegerField(null=True, blank=True, verbose_name=_('Badge size Y'))
    badge_color = ColorField(default='ffffff', verbose_name=_('Badge color'))
    template = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        ordering = ['-start']
        verbose_name = _("Event")
        verbose_name_plural = _("Events")

    def __unicode__(self):
        return self.name


class Field(models.Model):
    STATUS = (
            #('first_name', _('First name')), ('last_name', _('Last name')), ('email',_('E-mail')),
            ('document', _('Document')), ('phone', _('Telephone')),
            ('organization', _('Organization')), ('position', _('Position')),
            ('profession',_('Profession')), ('country',_('Country')),
    )
    event = models.ForeignKey('Event', related_name='fields', verbose_name=_('Event'))
    name = StatusField()
    label = models.CharField(max_length=100)
    order = models.IntegerField(null=True)

    class Meta:
        ordering = ['event', 'order']

    def __unicode__(self):
        return "%s : %s" % (self.event, self.name)


class Content(models.Model):
    event = models.ForeignKey('Event', related_name='contents', verbose_name=_('Event'))
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    image = FilerImageField(blank=True, null=True, verbose_name=_('Image'))
    title = models.CharField(max_length=200, verbose_name=_('Title'))
    STATUS = Choices(
        ('about',_('About')),
        ('confirmation', _('Confirmation')),
        ('contact',_('Contact')),
        ('info',_('Main description')),
        ('hotels', _('Hotels')),
        ('fieldtrip', _('Field Trip')),
        ('footer', _('Footer')),
        ('logistics', _('Logistics')),
        ('attendees', _('Attendees')),
        ('registration', _('Registration')),
        ('schedule', _('Schedule')),
        ('venue', _('Venue')),
        ('resources', _('Resources')),
        ('services', _('Services')),
        ('transportation', _('Transportation')),
        ('404',_('Not Found')),
        ('other', _('Other')),
    )
    page = StatusField()
    text = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = _("Content")
        verbose_name_plural = _("Contents")

    def __unicode__(self):
        return "%s: %s" % (self.event, self.name)


class Logo(models.Model):
    event = models.ForeignKey('Event', related_name='logos', verbose_name=_('Event'))
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    image = FilerImageField(verbose_name=_('Logo'))
    weight = models.IntegerField()
    url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ['weight']
        verbose_name = _("Logos")
        verbose_name_plural = _("Logos")

    def __unicode__(self):
        return self.name


class Activity(models.Model):
    #event = models.ForeignKey('Event', verbose_name=_('Event'))
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    slug = models.SlugField()
    organizer = models.ForeignKey('users.User', null=True, blank=True, verbose_name=_('Organizer'))
    text = models.TextField(blank=True,
                                 verbose_name=_('Activity description'),
                                 help_text='Try and enter few some more lines')
    image = FilerImageField(blank=True, null=True, related_name='activity_images', verbose_name=_('Image'))
    archivo = models.FileField(blank=True, null=True, upload_to='activity', verbose_name=_('File'))
    image_footer = FilerImageField(blank=True, null=True, related_name='activity_footers', verbose_name=_('Image footer'))
    start = models.DateTimeField(blank=True, null=True, verbose_name=_('Start'))
    end = models.DateTimeField(blank=True, null=True, verbose_name=_('End'))

    class Meta:
        ordering = ['start','name']
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
        ordering = ['name']
        verbose_name = _("Profession")
        verbose_name_plural = _("Professions")

    def __unicode__(self):
        return self.name

class PaymentMethod(models.Model):
    name = models.CharField(max_length=100, verbose_name=_('Name'))

    class Meta:
        ordering = ['name']
        verbose_name = _("Payment Method")
        verbose_name_plural = _("Payment Methods")

    def __unicode__(self):
        return self.name

class AttendeeTypeEvent(models.Model):
    attendeetype = models.ForeignKey('AttendeeType', verbose_name=_('Attendee Type'))
    event = models.ForeignKey('Event', verbose_name=_('Event'))
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_('Price'))
    eb_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_('Early Bird Price'))
    extra_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_('Extra Activity Price'))

    class Meta:
        verbose_name = _("Attendee Type in Event")
        verbose_name_plural = _("Attendee Types in Events")

class AttendeeType(models.Model):
    name = models.CharField(max_length=50, verbose_name=_('Name'))

    class Meta:
        ordering = ['name']
        verbose_name = _("Attendee Type")
        verbose_name_plural = _("Attendee Types")

    def __unicode__(self):
        return self.name

class AttendeeReceipt(models.Model):
    attendee = models.OneToOneField('Attendee', verbose_name=_('Attendee'), related_name='receipt')
    date = models.DateField(verbose_name=_('Date'))
    reference = models.CharField(max_length=20, verbose_name=_('Reference'))
    note = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Note'))

    class Meta:
        ordering = ['-date']
        verbose_name = _("Attendee Receipt")
        verbose_name_plural = _("Attendee Receipts")

    def __unicode__(self):
        return "%s" % (self.date,)


class AttendeePayment(models.Model):
    attendee = models.ForeignKey('users.User', verbose_name=_('Attendee'), related_name='payments')
    payment_method = models.ForeignKey('PaymentMethod', verbose_name=_('Payment Method'))
    date = models.DateField(verbose_name=_('Date'))
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Amount'))
    reference = models.CharField(max_length=20, verbose_name=_('Reference'))
    note = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Note'))

    class Meta:
        ordering = ['-date']
        verbose_name = _("Attendee Payment")
        verbose_name_plural = _("Attendee Payments")

    def __unicode__(self):
        return "%s" % (self.amount,)


class Font(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name=_('Name'))
    filename = models.CharField(max_length=250, unique=True, verbose_name=_('Filename'))

    class Meta:
        ordering = ['name']
        verbose_name = _("Font")
        verbose_name_plural = _("Fonts")

    def __unicode__(self):
        return self.name

class EventBadge(models.Model):
    event = models.ForeignKey('Event', verbose_name=_('Event'))
    FIELDS = (('event',_('Event')), ('name', _('Complete name')), ('first_name', _('First name')), ('last_name', _('Last name')),
            ('profession',_('Profession')), ('country',_('Country')), ('type',_('Type')), ('email',_('E-mail')), ('text', _('Text')),
            ('logo',_('Logo')), ('photo',_('Photo')), ('organization',_('Organization')))
    field = models.CharField(max_length=50, choices=FIELDS, verbose_name=_('Field'))
    color = ColorField(default='', null=True, blank=True, verbose_name=_('Color'))
    font = models.ForeignKey('Font', null=True, blank=True, verbose_name=_('Font'))
    size = models.IntegerField(verbose_name=_('Size'))
    x = models.IntegerField(verbose_name=_('X'))
    y = models.IntegerField(verbose_name=_('Y'))
    format = models.CharField(max_length=50, null=True, blank=True, verbose_name=_('Extra'))

    class Meta:
        ordering = ['field']
        verbose_name = _("Badge")
        verbose_name_plural = _("Badges")

    def __unicode__(self):
        return self.field


class Organization(models.Model):
    TYPE_CHOICES = Choices(('O', 'Organizador'), ('E', 'Exhibidor'), ('S', 'Speaker'))
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, null=True, blank=True)
    event = models.ForeignKey('Event', verbose_name=_('Event'))
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Name'))
    title = models.CharField(max_length=300, null=True, blank=True, verbose_name=_('Title'))
    place = models.CharField(max_length=300, null=True, blank=True, verbose_name=_('Place'))
    photo = models.ImageField(null=True, blank=True, verbose_name=_('Photo'))
    text = models.TextField(blank=True, verbose_name=_('Description'))
    url = models.URLField(null=True, blank=True)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Attendee(User):

    ORGANIZER = 1
    SPEAKER = 2
    SPONSOR = 3

    class Meta:
        ordering = ['first_name', 'last_name']
        verbose_name = _("Attendee")
        verbose_name_plural = _("Attendees")
        proxy = True

    def latest_payment(self):
       return self.payments.aggregate(max=Max('date'))['max']

    def paid(self):
       return self.payments.aggregate(sum=Sum('amount'))['sum']

    def earlybird_price(self):
        if not self.type or not self.event:
            return 'no type or event'
        try:
            price = self.event.attendeetypeevent_set.get(attendeetype=self.type).eb_price
            if self.extra:
                price += self.event.attendeetypeevent_set.get(attendeetype=self.type).extra_price
        except AttendeeTypeEvent.DoesNotExist:
            return 'wrong type'
        return price

    def regular_price(self):
        if not self.type or not self.event:
            return 'no type or event'
        try:
            price = self.event.attendeetypeevent_set.get(attendeetype=self.type).price
            if self.extra:
                price += self.event.attendeetypeevent_set.get(attendeetype=self.type).extra_price
        except AttendeeTypeEvent.DoesNotExist:
            return 'wrong type'
        return price

    def invited(self):
        test = Invited.objects.filter(email=self.email)
        if test:
            return True
        else:
            return False
    invited.short_description = _("Invited")
    invited.boolean = True

    def balance(self):
        price = self.price()
        if not self.payments.count():
            return price
        else:
            return price - self.paid()
    balance.short_description = _("Balance")

    def earlybird(self):
            if not self.event.eb_end:
                raise NameError('Event has no eb_end date')
            return self.paid() >= self.earlybird_price() and self.latest_payment() <= self.event.eb_end

    def price(self):
        if not self.type or not self.event:
            return 'no type or event'
        try:
            if self.earlybird():
                price = self.earlybird_price()
            else:
                price = self.regular_price()
            #if self.extra:
            #    price += self.event.attendeetypeevent_set.get(attendeetype=self.type).extra_price
        except AttendeeTypeEvent.DoesNotExist:
            return 'wrong type'
        return price
    price.short_description = _("Price")

    def short_full_name(self):
        return "%s %s" % (self.first_name.partition(' ')[0], self.last_name.partition(' ')[0])
    short_full_name.short_description = _("Name")

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)
    full_name.short_description = _("Name")

    def make_approved(modeladmin, request, queryset):
        queryset.update(approved=True)
    make_approved.short_description = _("Approve participation of selected attendees")

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)
