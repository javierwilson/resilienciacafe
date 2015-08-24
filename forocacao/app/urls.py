# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView

from .views import HomeView, ActivitiesView, AttendeeDetailView, event

urlpatterns = [
    url(r'^$', HomeView.as_view(), name="home"),
    url(r'^(?P<slug>[\w-]+)/activities/$', ActivitiesView.as_view(), name="activities"),
    url(r'^attendee/(?P<username>[\w.@+-]+)/$',AttendeeDetailView.as_view(), name='detail'),

    url(r'^(?P<url>.*/)$', event, name="event"),
]
