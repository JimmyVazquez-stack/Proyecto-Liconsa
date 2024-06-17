from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import TemplateView
from django.urls import reverse_lazy 
from django.views import generic
from .models import *
from .forms import TerminadoForm, permisosForm
from usuarios.utils.mixins import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

# Create your views here.
class index(LoginRequiredMixin,TemplateView, GroupRequiredMixin ):
    template_name = 'index.html'
    login_url = reverse_lazy('usuarios:login')

class grasas_aceites_vegetales(LoginRequiredMixin,TemplateView):
    template_name = 'grasas_aceites_vegetales.html'
    login_url = reverse_lazy('usuarios:login')

class mezcla_oleosa_vitaminas(LoginRequiredMixin,TemplateView):
    template_name = 'mezcla_oleosa_vitaminas.html'
    login_url = reverse_lazy('usuarios:login')

class pre_mezclas_vitaminas_minerales(LoginRequiredMixin,TemplateView):
    template_name = 'pre_mezclas_vitaminas_minerales.html'
    login_url = reverse_lazy('usuarios:login')

class leche_polvo_fysf(LoginRequiredMixin, TemplateView):
    template_name = 'leche_polvo_fysf.html'
    login_url = reverse_lazy('usuarios:login')

class soluciones_valoradas_ts(LoginRequiredMixin, TemplateView):
    template_name = 'soluciones_valoradas_ts.html'
    login_url = reverse_lazy('usuarios:login')

class evaluacion_sensorial(LoginRequiredMixin, TemplateView):
    template_name = 'evaluacion_sensorial.html'
    login_url = reverse_lazy('usuarios:login')

class monitoreo_medio_ambiente(LoginRequiredMixin, TemplateView):
    template_name = 'monitoreo_medio_ambiente.html'
    login_url = reverse_lazy('usuarios:login')

class limpieza_equipo_personal(LoginRequiredMixin, TemplateView):
    template_name = 'limpieza_equipo_personal.html'
    login_url = reverse_lazy('usuarios:login')

class calibracion_verificacion_equipo(LoginRequiredMixin, TemplateView):
    template_name = 'calibracion_verificacion_equipo.html'
    login_url = reverse_lazy('usuarios:login')

class verificacion_documentos(LoginRequiredMixin, TemplateView):
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
    login_url = reverse_lazy('usuarios:login')
    
