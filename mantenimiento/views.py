from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class index(LoginRequiredMixin, TemplateView):
    template_name = 'index.html'  
    login_url = 'usuarios:login'
    
class agua_alimentacion_proceso(LoginRequiredMixin,TemplateView):
    template_name = 'agua_alimentacion_proceso.html' 
    login_url = 'usuarios:login'