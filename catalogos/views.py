from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import LecheriaForm
from .models import Lecheria, Ruta, Poblacion, Area, Maquina
from django.http import JsonResponse
from django.views import View
from django.db.models import F 
from django.forms.models import model_to_dict
import json
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.
class LecheriaListView(LoginRequiredMixin,TemplateView):
    template_name = 'lecherias_list.html'
    login_url = reverse_lazy('usuarios:login')
    


class AñadirLecheriaView(LoginRequiredMixin, CreateView):
    template_name = 'añadir_lecheria.html'
    form_class = LecheriaForm
    login_url = reverse_lazy('usuarios:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    
class LecheriaDataView(LoginRequiredMixin,View):
    login_url = reverse_lazy('usuarios:login')
    def get(self, request, *args, **kwargs):
        lecherias = Lecheria.objects.annotate(
            numero_ruta=F('ruta__numero'),
            nombre_poblacion=F('poblacion__nombre'),
            rotos_reportados=F('rotos__rotos_reportados')
        ).values()  # Elimina los argumentos aquí
        lecherias_list = list(lecherias)
        return JsonResponse(lecherias_list, safe=False)
    

class ActualizarLecheriaView(View):
    login_url = reverse_lazy('usuarios:login')
    def post(self, request, *args, **kwargs):
        form_data = json.loads(request.body)
        lecheria = Lecheria.objects.get(id=form_data['id'])
        
        lecheria.numero = form_data.get('numero', lecheria.numero)
        lecheria.nombre = form_data.get('nombre', lecheria.nombre)
        lecheria.responsable = form_data.get('responsable', lecheria.responsable)
        lecheria.telefono = form_data.get('telefono', lecheria.telefono)
        lecheria.direccion = form_data.get('direccion', lecheria.direccion)
        
        ruta_id = form_data.get('ruta')
        if ruta_id is not None:
            lecheria.ruta = Ruta.objects.get(id=ruta_id)
        
        poblacion_id = form_data.get('poblacion')
        if poblacion_id is not None:
            lecheria.poblacion = Poblacion.objects.get(id=poblacion_id)
        
        lecheria.save()
        return JsonResponse(model_to_dict(lecheria), safe=False)
    
    
#Vistas de poblaciones

class PoblacionListView(LoginRequiredMixin,TemplateView):
    template_name = 'poblaciones/listar_poblaciones.html'
    login_url = reverse_lazy('usuarios:login')
    
    


class DataPoblacionView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def get(self, request, *args, **kwargs):
        poblaciones = Poblacion.objects.annotate(
            nombre_poblacion=F('nombre'),
            municipio_poblacion=F('municipio'),
            estado_poblacion=F('estado')
        ).values('id', 'nombre_poblacion', 'municipio_poblacion', 'estado_poblacion')
        
        poblaciones_list = list(poblaciones)
        return JsonResponse(poblaciones_list, safe=False)

#vistas de áreas

class AreaListView(LoginRequiredMixin,TemplateView):
    template_name = 'areas/listar_areas.html'
    login_url = reverse_lazy('usuarios:login')
    
class DataAreaView(LoginRequiredMixin,View):
    login_url = reverse_lazy('usuarios:login')
    def get(self, request, *args, **kwargs):
        areas = Area.objects.annotate(
            nombre_poblacion=F('poblacion__nombre'),
            nombre_lecheria=F('lecheria__nombre')
        ).values()  # Elimina los argumentos aquí
        areas_list = list(areas)
        return JsonResponse(areas_list, safe=False)
    
#vistas de maquinas

class MaquinaListView(LoginRequiredMixin,TemplateView):
    template_name = 'maquinas/listar_maquinas.html'
    login_url = reverse_lazy('usuarios:login')
    

class MaquinaDataView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')
    
    def get(self, request, *args, **kwargs):
        # Obtener todos los campos del modelo Maquina
        maquinas = Maquina.objects.annotate(
            nombre_planta=F('planta__nombre'),
        ).values()
        
        maquinas_list = list(maquinas)
        for maquina in maquinas_list:
            maquina['numero'] = f"Maquina-{maquina['numero']}"
        
        return JsonResponse(maquinas_list, safe=False)

#vistas de cabezales
class CabezalListView(LoginRequiredMixin,TemplateView):
    template_name = 'cabezales/listar_cabezales.html'
    login_url = reverse_lazy('usuarios:login')
    
#vistas de plantas
class PlantaListView(LoginRequiredMixin,TemplateView):
    template_name = 'plantas/listar_plantas.html'
    login_url = reverse_lazy('usuarios:login')
    
#vistas de proveedores
class ProveedorListView(LoginRequiredMixin,TemplateView):
    template_name = 'proveedores/listar_proveedores.html'
    login_url = reverse_lazy('usuarios:login')
    
#vistas de silos
class SiloListView(LoginRequiredMixin,TemplateView):
    template_name = 'silos/listar_silos.html'
    login_url = reverse_lazy('usuarios:login')
    
#vistas de turnos
class TurnoListView(LoginRequiredMixin,TemplateView):
    template_name = 'turnos/listar_turnos.html'
    login_url = reverse_lazy('usuarios:login')