from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


class index(LoginRequiredMixin,TemplateView):  
    template_name = 'index.html'
    login_url = 'usuarios:login'
    
class producto_silos(LoginRequiredMixin,TemplateView):
    template_name = 'producto_silos.html'
    login_url = 'usuarios:login'

class leche_fluida_salida_pasteurizador(LoginRequiredMixin,TemplateView):
    template_name = 'leche_fluida_salida_pasteurizador.html'
    login_url = 'usuarios:login'

class leche_fluida_envase_litros(LoginRequiredMixin,TemplateView):
    template_name = 'leche_fluida_envase_litros.html'
    login_url = 'usuarios:login'

class verificacion_contenido_neto(LoginRequiredMixin,TemplateView):
    template_name = 'verificacion_contenido_neto.html'
    login_url = 'usuarios:login'
    
class leche_cruda(LoginRequiredMixin  , TemplateView):
    template_name = 'leche_cruda.html'
    login_url = 'usuarios:login'

class leche_frisia_pipa(LoginRequiredMixin, TemplateView):
    template_name = 'leche_frisia_pipa.html'
    login_url = 'usuarios:login'

class concentracion_soluciones_materiales_limpieza(LoginRequiredMixin,TemplateView):
    template_name = 'concentracion_soluciones_materiales_limpieza.html'
    login_url = 'usuarios:login'