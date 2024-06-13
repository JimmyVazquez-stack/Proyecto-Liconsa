from django.shortcuts import render
from django.views.generic import TemplateView   
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class index(LoginRequiredMixin,TemplateView):
    template_name = 'index.html'
    login_url = 'usuarios:login'

class leche_polvo_fosf(LoginRequiredMixin,TemplateView):
    template_name = 'leche_polvo_fosf.html'
    login_url = 'usuarios:login'

class leche_cruda(LoginRequiredMixin,TemplateView):
    template_name = 'leche_cruda.html'
    login_url = 'usuarios:login'

class leche_frisia_pipa(LoginRequiredMixin,TemplateView):
    template_name = 'leche_frisia_pipa.html'
    login_url = 'usuarios:login'
 
class evaluacion_polietileno(TemplateView):
    template_name = 'evaluacion_polietileno.html'
    login_url = 'usuarios:login'

class solucion_alcalina(LoginRequiredMixin,TemplateView):
    template_name = 'solucion_alcalina.html'
    login_url = 'usuarios:login'

class solucion_acida(LoginRequiredMixin,TemplateView):
    template_name = 'solucion_acida.html'
    login_url = 'usuarios:login'

class hipoclorito_sodio(LoginRequiredMixin,TemplateView):
    template_name = 'hipoclorito_sodio.html'
    login_url = 'usuarios:login'
    