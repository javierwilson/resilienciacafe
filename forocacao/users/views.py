# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import base64
from PIL import Image, ImageDraw, ImageFont


from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import DetailView, ListView, RedirectView, UpdateView

from braces.views import LoginRequiredMixin
from easy_thumbnails.files import get_thumbnailer

from .models import User


class UserBadgeView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"
    def get(self, request, username):
        img = Image.new('RGBA', (600,400),(120,20,20))
        fnt = ImageFont.truetype('Pillow/Tests/fonts/FreeMono.ttf', 40)
        draw = ImageDraw.Draw(img)
        participant = self.get_object()
        x = 10
        y = 10
        draw.text((x,y), ("%s") % (participant.event), font=fnt, fill=(255,255,255,128))
        draw.text((x,y+50), ("%s %s") % (participant.first_name, participant.last_name), font=fnt, fill=(255,255,255,128))
        draw.text((x,y+50+50), ("%s") % (participant.profession), font=fnt, fill=(255,255,255,255))
        draw.text((x,y+50+50+50), ("%s") % (participant.country.name), font=fnt, fill=(255,255,255,255))
        if participant.event.logo:
            logo = Image.open(participant.event.logo.file.file)
            logo.thumbnail((200,200))
            img.paste(logo, (0,200))
        if participant.photo:
            photo = Image.open(participant.photo)
            photo.thumbnail((200,200))
            img.paste(photo, (400,200))
        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")
        return HttpResponse(response, content_type="image/png")

class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})


class UserUpdateView(LoginRequiredMixin, UpdateView):

    fields = ['name', 'phone', 'event', 'activities' ] #FIXME : add all needed fields

    # we already imported User in the view code above, remember?
    model = User

    # send the user back to their own page after a successful update
    def get_success_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})

    def get_object(self):
        # Only get the User record for the user making the request
        return User.objects.get(username=self.request.user.username)


class UserListView(LoginRequiredMixin, ListView):
    model = User
    # These next two lines tell the view to index lookups by username
    slug_field = "username"
    slug_url_kwarg = "username"
