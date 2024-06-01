from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class index(TemplateView):
    template_name = 'index.html'  

class agua_alimentacion_proceso(TemplateView):
    template_name = 'agua_alimentacion_proceso.html' 