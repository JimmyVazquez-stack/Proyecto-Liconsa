from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import LecheriaForm
from .models import Lecheria,  Rotos
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
from django.db.utils import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.db.models.functions import Concat
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views import View
from django.db.models import F, Value, CharField



# Create your views here.
class LecheriaListView(LoginRequiredMixin,TemplateView):
    template_name = 'lecherias/lecherias_list.html'
    login_url = reverse_lazy('usuarios:login')
    


class LecheriaDataView(LoginRequiredMixin,View):
    login_url = reverse_lazy('usuarios:login')
    def get(self, request, *args, **kwargs):
        lecherias = Lecheria.objects.annotate(
            nombre_ruta=F('ruta__nombre'),
            nombre_poblacion=F('poblacion__nombre'),
            ).values()  # Elimina los argumentos aquí
        lecherias_list = list(lecherias)
        return JsonResponse(lecherias_list, safe=False)
    

# Vista para crear una nueva lechería

class LecheriaCreateView(LoginRequiredMixin, CreateView):
    model = Lecheria
    form_class = LecheriaForm
    template_name = 'lecherias/lecheria_form.html'
    success_url = reverse_lazy('lecherias:list')
    login_url = reverse_lazy('usuarios:login')

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({'id': self.object.id, 'status': 'success'})

    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors, 'status': 'error'})

# Vista para actualizar una lechería existente
class LecheriaUpdateView(LoginRequiredMixin, UpdateView):
    model = Lecheria
    form_class = LecheriaForm
    template_name = 'lecherias/lecheria_form.html'
    success_url = reverse_lazy('lecherias:list')
    login_url = reverse_lazy('usuarios:login')

    def form_valid(self, form):
        self.object = form.save()
        return JsonResponse({'id': self.object.id, 'status': 'success'})

    def form_invalid(self, form):
        return JsonResponse({'errors': form.errors, 'status': 'error'})

# Vista para eliminar una lechería
class LecheriaDeleteView(LoginRequiredMixin, DeleteView):
    model = Lecheria
    success_url = reverse_lazy('lecherias:list')
    login_url = reverse_lazy('usuarios:login')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return JsonResponse({'status': 'success'})
    
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
    
class AreaCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        nombre = data.get('nombre')
        descripcion = data.get('descripcion')
        
        # Verificar si ya existe un área con el mismo nombre
        if Area.objects.filter(nombre=nombre).exists():
            return JsonResponse({'error': 'Ya existe un área con este nombre.'}, status=400)
        
        try:
            area = Area.objects.create(nombre=nombre, descripcion=descripcion)
            return JsonResponse({'id': area.id, 'nombre': area.nombre, 'descripcion': area.descripcion})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
        
class AreaUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        try:
            area = Area.objects.get(pk=pk)
            data = request.POST
            nombre = data.get('nombre')
            descripcion = data.get('descripcion')

            # Verificar si ya existe otra área con el mismo nombre
            if Area.objects.filter(nombre=nombre).exclude(pk=pk).exists():
                return JsonResponse({'error': 'Ya existe un área con este nombre.'}, status=400)

            area.nombre = nombre
            area.descripcion = descripcion
            area.save()
            return JsonResponse({'status': 'success', 'message': 'Área actualizada con éxito'})
        except Area.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Área no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


class AreaDeleteView(LoginRequiredMixin, View):
    def delete(self, request, pk, *args, **kwargs):
        try:
            area = Area.objects.get(pk=pk)
            area.delete()
            return JsonResponse({'status': 'success', 'message': 'Área eliminada con éxito'})
        except Area.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Área no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    
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


class MaquinaCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        data = request.POST
        numero = data.get('numero')
        nombre_planta = data.get('nombre_planta')
        try:
            maquina = Maquina.objects.create(numero=numero, nombre_planta=nombre_planta)
            return JsonResponse({'id': maquina.id, 'numero': maquina.numero, 'nombre_planta': maquina.nombre_planta})
        except IntegrityError:
            return JsonResponse({'error': 'Ya existe una maquina con este número.'}, status=400)

class MaquinaUpdateView(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        try:
            maquina = Maquina.objects.get(pk=pk)
            data = request.POST
            maquina.numero = data.get('numero')
            maquina.nombre_planta = data.get('nombre_planta')
            maquina.save()
            return JsonResponse({'status': 'success', 'message': 'Maquina actualizada con éxito'})
        except Maquina.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Maquina no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

class MaquinaDeleteView(LoginRequiredMixin, View):
    def delete(self, request, id, *args, **kwargs):
        try:
            maquina = Maquina.objects.get(pk=id)
            maquina.delete()
            return JsonResponse({'status': 'success', 'message': 'Maquina eliminada'})
        except Maquina.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Maquina no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)



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
    

class PlantaCreateView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def post(self, request, *args, **kwargs):
        data = request.POST
        nombre = data.get('nombre')
        ubicacion = data.get('ubicacion')
        correo = data.get('correo')
        contacto = data.get('contacto')
        telefono = data.get('telefono')

        if not (nombre and ubicacion and correo and contacto and telefono):
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

        try:
            planta = Planta.objects.create(
                nombre=nombre,
                ubicacion=ubicacion,
                correo=correo,
                contacto=contacto,
                telefono=telefono
            )
            return JsonResponse({
                'id': planta.id,
                'nombre': planta.nombre,
                'ubicacion': planta.ubicacion,
                'correo': planta.correo,
                'contacto': planta.contacto,
                'telefono': planta.telefono
            })
        except IntegrityError:
            return JsonResponse({'error': 'Error al crear la planta.'}, status=400)
        
# Vista para actualizar planta
class PlantaUpdateView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def post(self, request, pk, *args, **kwargs):
        planta = get_object_or_404(Planta, pk=pk)
        data = request.POST

        nombre = data.get('nombre')
        ubicacion = data.get('ubicacion')
        correo = data.get('correo')
        contacto = data.get('contacto')
        telefono = data.get('telefono')

        if not (nombre and ubicacion and correo and contacto and telefono):
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

        try:
            planta.nombre = nombre
            planta.ubicacion = ubicacion
            planta.correo = correo
            planta.contacto = contacto
            planta.telefono = telefono
            planta.save()
            return JsonResponse({'status': 'success', 'message': 'Planta actualizada con éxito'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        
        
class PlantaDeleteView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def delete(self, request, pk, *args, **kwargs):
        planta = get_object_or_404(Planta, pk=pk)
        try:
            planta.delete()
            return JsonResponse({'status': 'success', 'message': 'Planta eliminada'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

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
