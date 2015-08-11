from django.shortcuts import render
from django.views.generic import DetailView

from .models import Conference

class HomeView(DetailView):

    model = Conference
    template_name = "pages/home.html"

    def get_object(self):
        return Conference.objects.get(id=1)

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        return context
