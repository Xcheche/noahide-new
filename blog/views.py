from django.shortcuts import render
from django.views.generic import (TemplateView,ListView, DetailView)
# Create your views here.
# class HomeView(ListView):
#     template_name = 'blog/home.html'

class HomeView(TemplateView):
    template_name = 'blog/home.html'