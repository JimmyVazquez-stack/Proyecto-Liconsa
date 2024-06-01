from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class index(TemplateView):  
    template_name = 'index.html'

class producto_silos(TemplateView):
    template_name = 'producto_silos.html'

class leche_fluida_salida_pasteurizador(TemplateView):
    template_name = 'leche_fluida_salida_pasteurizador.html'

class leche_fluida_envase_litros(TemplateView):
    template_name = 'leche_fluida_envase_litros.html'

class verificacion_contenido_neto(TemplateView):
    template_name = 'verificacion_contenido_neto.html'

class leche_cruda(TemplateView):
    template_name = 'leche_cruda.html'

class leche_frisia_pipa(TemplateView):
    template_name = 'leche_frisia_pipa.html'

class concentracion_soluciones_materiales_limpieza(TemplateView):
    template_name = 'concentracion_soluciones_materiales_limpieza.html'
    