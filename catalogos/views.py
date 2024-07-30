from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .forms import LecheriaForm
from .models import Lecheria, Ruta, Poblacion, Maquina, Planta, Turno, Silo, Cabezal, Producto, TipoProducto, Proveedor
from usuarios.models import Area
from django.http import JsonResponse, HttpResponseNotAllowed
from django.views import View
from django.db.models import F, Value, CharField
from django.forms.models import model_to_dict
import json
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Concat
from django.db import IntegrityError


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
        areas = Area.objects.values()  # Elimina los argumentos aquí
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
    
class CabezalDataView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def get(self, request, *args, **kwargs):
        cabezales = Cabezal.objects.annotate(
            numero_maquina=Concat(Value('Maquina-'), F('maquina__numero'), output_field=CharField()),
            planta_maquina=F('maquina__planta__nombre'),
        ).values()  # Elimina la anotación aquí
        cabezales_list = list(cabezales)
        return JsonResponse(cabezales_list, safe=False)
    
#vistas de plantas
class PlantaListView(LoginRequiredMixin,TemplateView):
    template_name = 'plantas/listar_plantas.html'
    login_url = reverse_lazy('usuarios:login')
    
class PlantaDataView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def get(self, request, *args, **kwargs):
        plantas = Planta.objects.values()  # Elimina la anotación aquí
        plantas_list = list(plantas)
        return JsonResponse(plantas_list, safe=False)
    
#vistas de proveedores
class ProveedorListView(LoginRequiredMixin,TemplateView):
    template_name = 'proveedores/listar_proveedores.html'
    login_url = reverse_lazy('usuarios:login')
    
class ProveedorDataView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def get(self, request, *args, **kwargs):
        proveedores = Proveedor.objects.annotate(
            nombre_planta=F('planta__nombre'),
        ).values()  # Elimina la anotación aquí
        proveedores_list = list(proveedores)
        return JsonResponse(proveedores_list, safe=False)
    
#vistas de silos
class SiloListView(LoginRequiredMixin,TemplateView):
    template_name = 'silos/listar_silos.html'
    login_url = reverse_lazy('usuarios:login')
    
class DataSilosView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def get(self, request, *args, **kwargs):
        silos = Silo.objects.annotate(
            nombre_producto=F('producto__nombre'),
            nombre_planta=F('planta__nombre'),
        ).values()
        silos_list = list(silos)
        return JsonResponse(silos_list, safe=False)
    
#vistas de turnos
class TurnoListView(LoginRequiredMixin,TemplateView):
    template_name = 'turnos/listar_turnos.html'
    login_url = reverse_lazy('usuarios:login')

class TurnoDataView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def get(self, request, *args, **kwargs):
        turnos = Turno.objects.values()  # Elimina la anotación aquí
        turnos_list = list(turnos)
        return JsonResponse(turnos_list, safe=False)
    
#vistas para gestion de productos

class ProductoListView(LoginRequiredMixin,TemplateView):
    template_name = 'gestion_de_productos/listar_productos.html'
    login_url = reverse_lazy('usuarios:login')
    
class ProductoDataView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def get(self, request, *args, **kwargs):
        productos = Producto.objects.annotate(
            nombre_tipo_producto=F('tipo_producto__nombre'),
            ).values()  # Elimina la anotación aquí
        productos_list = list(productos)
        return JsonResponse(productos_list, safe=False)
    
    
class TipoProductoListView(LoginRequiredMixin,TemplateView):
    template_name = 'gestion_de_productos/listar_tipo_productos.html'
    login_url = reverse_lazy('usuarios:login')
    
class TipoProductoDataView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def get(self, request, *args, **kwargs):
        tipo_productos = TipoProducto.objects.values()  # Elimina la anotación aquí
        tipo_productos_list = list(tipo_productos)
        return JsonResponse(tipo_productos_list, safe=False)
    
#vistas para rutas
class RutaListView(LoginRequiredMixin,TemplateView):
    template_name = 'rutas/listar_rutas.html'
    login_url = reverse_lazy('usuarios:login')
    
class RutaDataView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def get(self, request, *args, **kwargs):
        rutas = Ruta.objects.values()  # Elimina la anotación aquí
        rutas_list = list(rutas)
        return JsonResponse(rutas_list, safe=False)
    
class RutaCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        nombre = data.get('nombre')
        numero = data.get('numero')
        try:
            ruta = Ruta.objects.create(nombre=nombre, numero=numero)
            return JsonResponse({'id': ruta.id, 'nombre': ruta.nombre, 'numero': ruta.numero})
        except IntegrityError:
            return JsonResponse({'error': 'Ya existe una ruta con este número.'}, status=400)

class RutaUpdateView(View):
    def post(self, request, pk, *args, **kwargs):
        try:
            ruta = Ruta.objects.get(pk=pk)
            data = request.POST
            ruta.nombre = data.get('nombre')
            ruta.numero = data.get('numero')
            ruta.save()
            return JsonResponse({'status': 'success', 'message': 'Ruta actualizada con éxito'})
        except Ruta.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Ruta no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
# Vista
class RutaDeleteView(LoginRequiredMixin, View):
    def delete(self, request, id, *args, **kwargs):
        ruta = Ruta.objects.get(pk=id)
        ruta.delete()  # Asegúrate de que esto elimine la ruta de la base de datos
        return JsonResponse({'status': 'success', 'message': 'Ruta eliminada'})
