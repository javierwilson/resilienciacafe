# -*- coding: utf-8 -*-
from datetime import date
from PIL import Image, ImageDraw, ImageFont

from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.conf import settings
from django.template.defaultfilters import date as _date
from django.utils import timezone

from braces.views import LoginRequiredMixin
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.graphics.barcode import qr
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

from .models import Event, Activity, Attendee, AttendeeReceipt, Content



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
        return self.model.objects.get(event__slug=self.kwargs['slug'], page=self.page)

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
    canvas = canvas.Canvas(response)
    canvas.pagesize = letter

    def draw(self, string, x, y, color=colors.black, font='Helvetica', size=12):
        self.canvas.setFillColor(color)
        self.canvas.setFont(font, size)
        self.canvas.drawString(x, y, string)

    def get(self, request, username):
        participant = self.get_object()

        self.canvas.setTitle("%s : %s" % (participant.event.name, participant.full_name()))
        width, height = letter
        y = hstart = height-20
        x = wstart = 120

        self.draw("Evento", x, y, size=10, color=colors.grey)
        y -= 20
        self.draw(participant.event.name, x, y, size=22)
        y -= 20

        self.draw("Fecha y Hora", x, y, size=10, color=colors.grey)
        y -= 20
        self.draw(_date(timezone.localtime(participant.event.start), 'r'), x, y)
        y += 20

        self.draw("Ubicación", x+200, y, size=10, color=colors.grey)
        y -= 20
        self.draw(participant.event.place, x+200, y)
        y -= 20

        self.draw("Participante", x, y, size=10, color=colors.grey)
        y -= 20
        self.draw(participant.full_name(), x, y)
        y += 20

        self.draw("Organización", x+200, y, size=10, color=colors.grey)
        y -= 20
        self.draw(participant.organization, x+200, y)
        y -= 20

        self.draw(u"País", x, y, size=10, color=colors.grey)
        y -= 20
        self.draw(str(participant.country.name), x, y)
        y += 20

        self.draw("Cargo", x+200, y, size=10, color=colors.grey)
        y -= 20
        self.draw(participant.position, x+200, y)
        y += 20

        # insert logo
        logo = Image.open(participant.event.logo.file.file)
        logo_width = logo.size[0]
        logo_height = logo.size[1]
        #logo._restrictSize(2 * inch, 1 * inch)
        #logo.thumbnail((120,100))
        logo = participant.event.logo.file.file.name
        self.canvas.drawImage(logo, wstart-100, hstart-(logo_height/2), width=logo_width/2, height=logo_height/2)

        # draw a QR code
        contact = {
            'name': "%s: %s" % (participant.id, participant.full_name()),
            'phone_number': participant.phone,
            'email': participant.email,
            'url': reverse('app:detail', kwargs={'username': participant.username}),
            'company': participant.organization,
        }
        qr_code = qr.QrCodeWidget(contact['name'])
        bounds = qr_code.getBounds()
        width = bounds[2] - bounds[0]
        height = bounds[3] - bounds[1]
        d = Drawing(100, 100, transform=[100./width,0,0,100./height,0,0])
        d.add(qr_code)
        renderPDF.draw(d, self.canvas, wstart+320, y)

        self.canvas.showPage()
        self.canvas.save()

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
