from django.shortcuts import render
from django.views.generic.base import TemplateView
# Create your views here.


class MainView(TemplateView):
    template_name = "common/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
