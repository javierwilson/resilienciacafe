# -*- coding: utf-8 -*-
from datetime import date
from PIL import Image, ImageDraw, ImageFont

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.conf import settings

from braces.views import LoginRequiredMixin

from .models import Event, Activity, Attendee, AttendeeReceipt, Content
from .pdf import createPDF


class HomeView(DetailView):

    model = Event
    template_name = "pages/home.html"

    def get_object(self):
        return Event.objects.filter(status='frontpage')[0]

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context


class ContentView(DetailView):
    model = Content
    page = None

    def get_object(self):
        if self.kwargs:
            return self.model.objects.get(event__slug=self.kwargs['slug'], page=self.page)
        else:
            #FIXME qué si hay varios eventos?
            return self.model.objects.get(page=self.page)


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
        createPDF(self.get_object(), self.response)
        return self.response



class AttendeeJPEGView(LoginRequiredMixin, DetailView):
    model = Attendee
    slug_field = "username"
    slug_url_kwarg = "username"

    def get(self, request, username):
        participant = self.get_object()
        event = participant.event

        img = Image.new('RGBA', (event.badge_size_x, event.badge_size_y), event.badge_color)
        draw = ImageDraw.Draw(img)

        match = {
                'event': event.name,
                'name': "%s %s" % (participant.first_name, participant.last_name ),
                'first_name': participant.first_name,
                'last_name': participant.last_name,
                'profession': participant.profession,
                'country': participant.country.name,
                'type': participant.type,
                'email': participant.email,
            }
        for field in event.eventbadge_set.all():
            x = field.x
            y = field.y
            size = field.size
            if field.field == 'logo':
                if participant.event.logo:
                    logo = Image.open(participant.event.logo.file.file)
                    logo.thumbnail((size,size))
                    img.paste(logo, (x,y))
            elif field.field == 'photo':
                if participant.photo:
                    photo = Image.open(participant.photo)
                    photo.thumbnail((size,size))
                    img.paste(photo, (x,y))
            else:
                if field.field == 'text':
                    content = field.format
                else:
                    content = match[field.field]
                fnt = ImageFont.truetype(field.font.filename, size)
                color = field.color
                draw.text((x,y), ("%s") % (content), font=fnt, fill=color)


        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")
        return HttpResponse(response, content_type="image/png")



class AttendeeBadgeView(LoginRequiredMixin, DetailView):
    model = Attendee
    slug_field = "username"
    slug_url_kwarg = "username"
    template_name = "app/attendee_badge.html"

class AttendeeDetailView(LoginRequiredMixin, DetailView):
    model = Attendee
    slug_field = "username"
    slug_url_kwarg = "username"


class ActivitiesView(ListView):

    model = Activity

    def get_queryset(self):
        return Activity.objects.filter(event__slug=self.kwargs['slug'])

    def get_context_data(self, **kwargs):
        context = super(ActivitiesView, self).get_context_data(**kwargs)
        context['event'] = Event.objects.get(slug=self.kwargs['slug'])
        return context

def event(request, url):
    #if not url.startswith('/'):
    #    url = '/' + url
    template_name = "pages/home.html"
    if url.endswith('/'):
        url = url[:-1]
    print "---------------------------------"
    print url
    try:
        f = get_object_or_404(Event, slug=url)
    except Http404:
        if not url.endswith('/') and settings.APPEND_SLASH:
            url += '/'
            f = get_object_or_404(Event, slug=url)
            return HttpResponsePermanentRedirect('%s/' % request.path)
        else:
            raise
    return render(request, template_name, context={'object': f})
