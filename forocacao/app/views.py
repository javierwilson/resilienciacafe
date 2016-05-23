# -*- coding: utf-8 -*-
from datetime import date

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.conf import settings

from braces.views import LoginRequiredMixin

from .models import Event, Activity, Attendee, AttendeeReceipt, Content, Logo
from .pdf import createPDF
from .png import createPNG


class HomeView(DetailView):

    model = Event
    template_name = "pages/home.html"

    def get_object(self, **kwargs):
        try:
            object = super(HomeView, self).get_object(**kwargs)
        except AttributeError:
            object = Event.objects.filter(status='frontpage')[0]
        return object

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['logos'] = Logo.objects.filter(event=self.object)
        return context


class ContentView(DetailView):
    model = Content
    page = None

    def get_object(self):
        if self.kwargs:
            return get_object_or_404(self.model, event__slug=self.kwargs['slug'], page=self.page)
        else:
            #FIXME qué si hay varios eventos?
            return get_object_or_404(self.model, page=self.page)


class AttendeeReceiptView(LoginRequiredMixin, DetailView):
    model = AttendeeReceipt

    def get_object(self):
        try:
            attendee = Attendee.objects.get(username=self.kwargs.get("username"))
            if attendee.balance() > 0:
                raise NameError('Balance > 0')
            receipt = AttendeeReceipt.objects.get(attendee__username=self.kwargs.get("username"))
            return receipt
        except AttendeeReceipt.DoesNotExist:
            attendee = Attendee.objects.get(username=self.kwargs.get("username"))
            new_receipt = AttendeeReceipt(attendee=attendee, date=date.today())
            new_receipt.save()
            return new_receipt


class AttendeePDFView(LoginRequiredMixin, DetailView):
    model = Attendee
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "app/attendee_badge.html"
    response = HttpResponse(content_type="application/pdf")

    def get(self, request, username):
        self.response = HttpResponse(content_type="application/pdf")
        createPDF(self.get_object(), self.response)
        return self.response


class AttendeePNGView(LoginRequiredMixin, DetailView):
    model = Attendee
    slug_field = "username"
    slug_url_kwarg = "username"
    response = HttpResponse(content_type="image/png")

    def get(self, request, username):
        self.response = HttpResponse(content_type="image/png")
        createPNG(self.get_object(), self.response)
        return self.response


class AttendeeBadgeView(LoginRequiredMixin, DetailView):
    model = Attendee
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "app/attendee_badge.html"


class AttendeeDetailView(LoginRequiredMixin, DetailView):
    model = Attendee
    slug_field = "username"
    slug_url_kwarg = "username"


class SpeakersDetailView(DetailView):

    model = Attendee
    template_name = 'app/speaker_detail.html'
    slug_field = 'username'

    def get_context_data(self, **kwargs):
        context = super(SpeakersDetailView, self).get_context_data(**kwargs)
        context['event'] = Event.objects.get(slug=self.kwargs['eventslug'])
        return context

class SpeakersView(ListView):

    model = Attendee
    template_name = 'app/speaker_list.html'

    def get_queryset(self):
        return Attendee.objects.filter(event__slug=self.kwargs['slug'], type=Attendee.SPEAKER)

    def get_context_data(self, **kwargs):
        context = super(SpeakersView, self).get_context_data(**kwargs)
        context['event'] = Event.objects.get(slug=self.kwargs['slug'])
        return context

#class ActivitiesView(LoginRequiredMixin, ListView):
class ActivitiesView(ListView):

    model = Activity

    def get_queryset(self):
        return Activity.objects.filter(event__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(ActivitiesView, self).get_context_data(**kwargs)
        context['event'] = Event.objects.get(slug=self.kwargs['slug'])
        return context

# orphan
def event(request,slug):
    #if not url.startswith('/'):
    #    url = '/' + url
    template_name = "pages/event.html"
    if slug.endswith('/'):
        slug = slug[:-1]
    try:
        f = get_object_or_404(Event, slug=slug)
    except Http404:
        if not slug.endswith('/') and settings.APPEND_SLASH:
            slug += '/'
            f = get_object_or_404(Event, slug=slug)
            return HttpResponsePermanentRedirect('%s/' % request.path)
        else:
            raise
    return render(request, template_name, context={'object': f})
