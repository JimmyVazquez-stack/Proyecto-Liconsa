from django.shortcuts import render
from django.views.generic import TemplateView
from laboratorio_control_calidad.forms import TablaR49Form, DensidadptForm, PesoenvvacioForm, PesobrutoForm #PesonetoForm
from .models import TablaR49, Densidadpt, Pesoenvvacio, Pesobruto #Pesoneto
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic 

# Create your views here.
# class index(LoginRequiredMixin,TemplateView, GroupRequiredMixin ):
#     template_name = 'index.html'
#     login_url = reverse_lazy('usuarios:login')

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




## CRUD FormatoR49 Juan Carlos M.

class registror49_list(generic.ListView):
     model = TablaR49
     queryset = TablaR49.objects.all ()
     template_name = 'registror49_list.html'
     context_object_name = 'tablar49'

class registror49_create(generic.CreateView):
    model = TablaR49
    template_name = 'registror49_create.html'
    context_object_name = 'tablar49'
    form_class = TablaR49Form
    success_url = reverse_lazy("laboratorio_control_calidad:registror49_list")

class registror49_update(generic.UpdateView):
    model = TablaR49
    template_name = 'registror49_create.html' 
    form_class = TablaR49Form
    success_url = reverse_lazy('laboratorio_control_calidad:registror49_list')
    context_object_name = 'tablar49'

class registror49_delete(generic.DeleteView):
    model = TablaR49
    template_name = 'registror49_delete.html'
    context_object_name = 'tablar49'
    success_url = reverse_lazy('laboratorio_control_calidad:registror49_list')

### complementarias a formato R49 DENSIDAD

class densidadr49_list(generic.ListView):
     model = Densidadpt
     queryset = Densidadpt.objects.all ()
     template_name = 'densidadr49_list.html'
     context_object_name = 'densidadr49'

class densidadr49_create(generic.CreateView):
    model = Densidadpt
    template_name = 'densidadr49_create.html'
    context_object_name = 'densidadr49'
    form_class = DensidadptForm
    success_url = reverse_lazy("laboratorio_control_calidad:densidadr49_list")

class densidadr49_update(generic.UpdateView):
    model = Densidadpt
    template_name = 'densidadr49_create.html' 
    form_class = DensidadptForm
    success_url = reverse_lazy('laboratorio_control_calidad:densidadr49_list')
    context_object_name = 'densidadr49'

class densidadr49_delete(generic.DeleteView):
    model = Densidadpt
    template_name = 'densidadr49_delete.html'
    context_object_name = 'densidadr49'
    success_url = reverse_lazy('laboratorio_control_calidad:densidadr49_list')


### complementarias a formato R49 PESO ENVASE VACIO
class pesoenvvacior49_list(generic.ListView):
     model = Pesoenvvacio
     queryset = Pesoenvvacio.objects.all ()
     template_name = 'complementariasR49/pesoenvvacior49_list.html'
     context_object_name = 'pesoenvvacior49'

class pesoenvvacior49_create(generic.CreateView):
    model = Pesoenvvacio
    template_name = 'complementariasR49/pesoenvvacior49_create.html'
    context_object_name = 'pesoenvvacior49'
    form_class = PesoenvvacioForm
    success_url = reverse_lazy('laboratorio_control_calidad:pesoenvvacior49_list')

class pesoenvvacior49_update(generic.UpdateView):
    model = Pesoenvvacio
    template_name = 'complementariasR49/pesoenvvacior49_create.html' 
    form_class = PesoenvvacioForm
    success_url = reverse_lazy('laboratorio_control_calidad:pesoenvvacior49_list')
    context_object_name = 'pesoenvvacior49'

class pesoenvvacior49_delete(generic.DeleteView):
    model = Pesoenvvacio
    template_name = 'complementariasR49/pesoenvvacior49_delete.html'
    context_object_name = 'densidadr49'
    success_url = reverse_lazy('laboratorio_control_calidad:pesoenvvacior49_list')

### complementarias a formato R49 PESO BRUTO
class pesobrutor49_list(generic.ListView):
     model = Pesobruto
     queryset = Pesobruto.objects.all ()
     template_name = 'complementariasR49/pesobrutor49_list.html'
     context_object_name = 'pesobrutor49'

class pesobrutor49_create(generic.CreateView):
    model = Pesobruto
    template_name = 'complementariasR49/pesobrutor49_create.html'
    context_object_name = 'pesobrutor49'
    form_class = PesobrutoForm
    success_url = reverse_lazy("laboratorio_control_calidad:pesobrutor49_list")

class pesobrutor49_update(generic.UpdateView):
    model = Pesobruto
    template_name = 'complementariasR49/pesobrutor49_create.html' 
    form_class = PesobrutoForm
    success_url = reverse_lazy('laboratorio_control_calidad:pesobrutor49_list')
    context_object_name = 'pesobrutor49'

class pesobrutor49_delete(generic.DeleteView):
    model = Pesobruto
    template_name = 'complementariasR49/pesobrutor49_delete.html'
    context_object_name = 'pesobrutor49'
    success_url = reverse_lazy('laboratorio_control_calidad:pesobrutor49_list')

