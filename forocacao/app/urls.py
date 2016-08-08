# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView, DetailView, ListView

from .models import Event, Organization
from .views import HomeView, SpeakersView, SpeakersDetailView, ActivitiesView, AttendeeDetailView, AttendeeBadgeView, AttendeePNGView, AttendeePDFView, AttendeeReceiptView, ContentView, event, OrganizationsView

urlpatterns = [

    # pics
    url(r'^photologue/', include('photologue.urls', namespace='photologue')),

    # home
    url(r'^$', HomeView.as_view(), name='home'),

    # content
    url(r'^(?P<slug>[\w-]+)/confirmation/$', ContentView.as_view(page='confirmation'), name='confirmation'),
    url(r'^confirmation/$', ContentView.as_view(page='confirmation'), name='confirmationmail'),
    url(r'^(?P<slug>[\w-]+)/about/$', ContentView.as_view(page='about'), name='about'),
    # FIXME: services?
    url(r'^(?P<slug>[\w-]+)/services/$', ContentView.as_view(page='services'), name='services'),
    url(r'^(?P<slug>[\w-]+)/contact/$', ContentView.as_view(page='contact'), name='contact'),
    # FIXME: necesitamos esto como flatpage?
    url(r'^(?P<slug>[\w-]+)/attendees/$', ContentView.as_view(page='attendees'), name='attendees'),
    url(r'^(?P<slug>[\w-]+)/fieldtrip/$', ContentView.as_view(page='fieldtrip'), name='fieldtrip'),
    url(r'^(?P<slug>[\w-]+)/schedule/$', ContentView.as_view(page='schedule'), name='schedule'),
    # new contect 2016
    url(r'^(?P<slug>[\w-]+)/venue/$', ContentView.as_view(page='venue'), name='venue'),
    url(r'^(?P<slug>[\w-]+)/hotels/$', ContentView.as_view(page='hotels'), name='hotels'),
    url(r'^(?P<slug>[\w-]+)/transportation/$', ContentView.as_view(page='transportation'), name='transportation'),

    # activities
    url(r'^(?P<slug>[\w-]+)/activities/$', ActivitiesView.as_view(), name='activities'),

    # speakers
    url(r'^(?P<slug>[\w-]+)/organizadores/$', OrganizationsView.as_view(title=u'Orgnizadores', filter='O'), name='organizers'),
    url(r'^(?P<slug>[\w-]+)/exhibicion/$', OrganizationsView.as_view(title=u'Area de exhibición', filter='E'), name='exhibition'),
    url(r'^(?P<slug>[\w-]+)/speakers/$', SpeakersView.as_view(), name='speakers'),
    url(r'^(?P<eventslug>[\w-]+)/speakers/(?P<slug>[\w-]+)/$', SpeakersDetailView.as_view(), name='speakers-detail'),

    # profiles
    url(r'^attendee/(?P<username>[\w.@+-]+)/$',AttendeeDetailView.as_view(), name='detail'),
    url(r'^attendee/(?P<username>[\w.@+-]+)/badge/$',AttendeeBadgeView.as_view(), name='badge'),
    url(r'^attendee/(?P<username>[\w.@+-]+)/png/$',AttendeePNGView.as_view(), name='png'),
    url(r'^attendee/(?P<username>[\w.@+-]+)/pdf/$',AttendeePDFView.as_view(), name='pdf'),
    url(r'^attendee/(?P<username>[\w.@+-]+)/receipt/$',AttendeeReceiptView.as_view(), name='receipt'),

    # events
    url(r'^events/$', ListView.as_view(model=Event), name='events'),
    url(r'^(?P<slug>[\w-]+)/$', HomeView.as_view(), name='event'),
]
