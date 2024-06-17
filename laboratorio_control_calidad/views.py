from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy 
from django.views import generic
from .models import *
from .forms import TerminadoForm, permisosForm

# Create your views here.
class index(TemplateView):
    template_name = 'index.html'

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

class TerminadoCreate(generic.CreateView):
    model = producto_terminado
    template_name = 'producto_terminado.html'
    context_object_name = 'terminado'
    form_class = TerminadoForm
    success_url = reverse_lazy("laboratorio_control_calidad:TerminadoList")

class producto_terminado_list(generic.ListView):
    model = producto_terminado
    queryset = producto_terminado.objects.all()
    template_name = 'producto_terminadoList.html'
    context_object_name = 'terminado'

class TerminadoUpdate(generic.UpdateView):
    model = producto_terminado
    template_name = 'producto_terminado.html'
    context_object_name = 'terminado'
    form_class = TerminadoForm
    success_url = reverse_lazy('laboratorio_control_calidad:TerminadoList')

class TerminadoDelete(generic.DeleteView):
    model = producto_terminado
    template_name = 'terminadoDelete.html'
    context_object_name = 'terminado'
    success_url = reverse_lazy('laboratorio_control_calidad:TerminadoList')

class permisos(generic.UpdateView):
    model = producto_terminado
    form_class = permisosForm
    template_name = "modificar.html"
    success_url = reverse_lazy('laboratorio_control_calidad:TerminadoList')