from django.http import Http404, HttpResponse, HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.conf import settings

from braces.views import LoginRequiredMixin

from .models import Event, Activity, Attendee, AttendeeReceipt

class HomeView(DetailView):

    model = Event
    template_name = "pages/home.html"

    def get_object(self):
        return Event.objects.filter(status='frontpage')[0]

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context


class AttendeeReceiptView(LoginRequiredMixin, DetailView):
    model = AttendeeReceipt


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
