from django.shortcuts import render
from django.views.generic import TemplateView   
# Create your views here.


class index(TemplateView):
    template_name = 'index.html'

class leche_polvo_fosf(TemplateView):
    template_name = 'leche_polvo_fosf.html'

class leche_cruda(TemplateView):
    template_name = 'leche_cruda.html'

class leche_frisia_pipa(TemplateView):
    template_name = 'leche_frisia_pipa.html'
 
class evaluacion_polietileno(TemplateView):
    template_name = 'evaluacion_polietileno.html'

class solucion_alcalina(TemplateView):
    template_name = 'solucion_alcalina.html'

class solucion_acida(TemplateView):
    template_name = 'solucion_acida.html'

class hipoclorito_sodio(TemplateView):
    template_name = 'hipoclorito_sodio.html'
    