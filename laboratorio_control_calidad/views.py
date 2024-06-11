from django.shortcuts import render
from django.views.generic import TemplateView
from usuarios.utils.mixins import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class index(TemplateView, GroupRequiredMixin, LoginRequiredMixin):
    template_name = 'index.html'
    group_names = ['Coordinador', 'Jefe de Unidad']

class grasas_aceites_vegetales(TemplateView):
    template_name = 'grasas_aceites_vegetales.html'

class mezcla_oleosa_vitaminas(TemplateView):
    template_name = 'mezcla_oleosa_vitaminas.html'

class pre_mezclas_vitaminas_minerales(TemplateView):
    template_name = 'pre_mezclas_vitaminas_minerales.html'

class leche_polvo_fysf(TemplateView):
    template_name = 'leche_polvo_fysf.html'

class soluciones_valoradas_ts(TemplateView):
    template_name = 'soluciones_valoradas_ts.html'

class evaluacion_sensorial(TemplateView):
    template_name = 'evaluacion_sensorial.html'

class monitoreo_medio_ambiente(TemplateView):
    template_name = 'monitoreo_medio_ambiente.html'

class limpieza_equipo_personal(TemplateView):
    template_name = 'limpieza_equipo_personal.html'

class calibracion_verificacion_equipo(TemplateView):
    template_name = 'calibracion_verificacion_equipo.html'

class verificacion_documentos(TemplateView):
    template_name = 'verificacion_documentos.html'
    