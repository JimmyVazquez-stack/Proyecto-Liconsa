#Importaciones modelos
from .models import (Lecheria, Ruta, Poblacion, Maquina, Planta, Turno, Silo, Cabezal, Producto, TipoProducto, Proveedor, Turno, Lecheria)
from usuarios.models import Area
from django.db.models import F, Value, CharField, Q
from django.db.models.functions import Concat
#Importaciones forms
from .forms import LecheriaForm
#Importaciones de vistas
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import View
#Otras importaciones
from django.shortcuts import get_object_or_404
from django.views import View
#Otras importaciones
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.http import JsonResponse
from django.db.utils import IntegrityError
from django.contrib.auth.mixins import LoginRequiredMixin
#uso en modelo createSilos
from django.db import transaction
#importacion para modelo turno
from django.utils.dateparse import parse_time
from datetime import time, datetime
from django.core.exceptions import ValidationError
from django.http import QueryDict





# Create your views here.
class LecheriaListView(LoginRequiredMixin, TemplateView):
    template_name = 'lecherias/lecherias_list.html'
    login_url = reverse_lazy('usuarios:login')



class LecheriaDataView(LoginRequiredMixin, View):
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

# Vistas de poblaciones


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

# Vistas de poblaciones


class PoblacionListView(LoginRequiredMixin, TemplateView):
    template_name = 'poblaciones/listar_poblaciones.html'
    login_url = reverse_lazy('usuarios:login')


class DataPoblacionView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')
    def get(self, request, *args, **kwargs):
        poblaciones = Poblacion.objects.values()
        poblaciones = Poblacion.objects.values()
        poblaciones_list = list(poblaciones)
        return JsonResponse(poblaciones_list, safe=False)
    

class PoblacionCreateView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def post(self, request, *args, **kwargs):
        data = request.POST
        nombre = data.get('nombre')
        municipio = data.get('municipio')
        estado = data.get('estado')

        if not (nombre and municipio and estado):
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

        try:
            poblacion = Poblacion.objects.create(
                nombre=nombre,
                municipio=municipio,
                estado=estado
            )
            return JsonResponse({
                'id': poblacion.id,
                'nombre': poblacion.nombre,
                'municipio': poblacion.municipio,
                'estado': poblacion.estado
            })
        except IntegrityError:
            return JsonResponse({'error': 'Error al crear la población.'}, status=400)
        
class PoblacionUpdateView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def post(self, request, pk, *args, **kwargs):
        poblacion = get_object_or_404(Poblacion, pk=pk)
        data = request.POST

        nombre = data.get('nombre')
        municipio = data.get('municipio')
        estado = data.get('estado')

        if not (nombre and municipio and estado):
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

        try:
            poblacion.nombre = nombre
            poblacion.municipio = municipio
            poblacion.estado = estado
            poblacion.save()
            return JsonResponse({'status': 'success', 'message': 'Población actualizada con éxito'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        
class PoblacionDeleteView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def delete(self, request, pk, *args, **kwargs):
        poblacion = get_object_or_404(Poblacion, pk=pk)
        try:
            poblacion.delete()
            return JsonResponse({'status': 'success', 'message': 'Población eliminada'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

#vistas de áreas
class AreaListView(LoginRequiredMixin,TemplateView):
    template_name = 'areas/listar_areas.html'
    login_url = reverse_lazy('usuarios:login')




class DataAreaView(LoginRequiredMixin, View):
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

# vistas de maquinas


class MaquinaListView(LoginRequiredMixin, TemplateView):
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


        return JsonResponse(maquinas_list, safe=False)

class MaquinaCreateView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def post(self, request, *args, **kwargs):
        data = request.POST
        numero = data.get('numero')
        planta_id = data.get('nombre_planta')

        if not (numero and planta_id):
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

        try:
            planta = Planta.objects.get(id=planta_id)
            
            # Verificar si ya existe una máquina con el mismo número en la misma planta
            if Maquina.objects.filter(numero=numero, planta=planta).exists():
                return JsonResponse({'error': 'Ya existe una máquina con este número en la planta seleccionada.'}, status=400)
            
            maquina = Maquina.objects.create(numero=numero, planta=planta)
            return JsonResponse({'id': maquina.id, 'numero': maquina.numero, 'nombre_planta': planta.nombre})
        except Planta.DoesNotExist:
            return JsonResponse({'error': 'La planta seleccionada no existe.'}, status=400)
        except IntegrityError:
            return JsonResponse({'error': 'Error al guardar la máquina.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': f'Error desconocido: {str(e)}'}, status=500)

class MaquinaUpdateView(LoginRequiredMixin, View):
    def put(self, request, pk, *args, **kwargs):
        data = request.POST

        # Cambiar el acceso a data para usar request.body si se está usando PUT
        if request.method == 'PUT':
            data = QueryDict(request.body)

        numero = data.get('numero')
        planta_id = data.get('nombre_planta')

        if not (numero and planta_id):
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

        try:
            planta = Planta.objects.get(id=planta_id)

            # Verificar si ya existe una máquina con el mismo número en la misma planta, excluyendo la actual
            if Maquina.objects.filter(numero=numero, planta=planta).exclude(pk=pk).exists():
                return JsonResponse({'error': 'Ya existe una máquina con este número en la planta seleccionada.'}, status=400)

            maquina = get_object_or_404(Maquina, pk=pk)
            maquina.numero = numero
            maquina.planta = planta
            maquina.save()
            return JsonResponse({'id': maquina.id, 'numero': maquina.numero, 'nombre_planta': planta.nombre})
        except Planta.DoesNotExist:
            return JsonResponse({'error': 'La planta seleccionada no existe.'}, status=400)
        except Maquina.DoesNotExist:
            return JsonResponse({'error': 'Máquina no encontrada'}, status=404)
        except IntegrityError:
            return JsonResponse({'error': 'Error al guardar la máquina.'}, status=400)

        return JsonResponse({'error': 'Error desconocido.'}, status=500)

class MaquinaDeleteView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    login_url = reverse_lazy('usuarios:login')

    def delete(self, request, id, *args, **kwargs):
        try:
            maquina = Maquina.objects.get(pk=id)
            maquina.delete()
            return JsonResponse({'status': 'success', 'message': 'Maquina eliminada'})
        except Maquina.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Maquina no encontrada'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        
        # Asegurarse de que siempre se devuelva una respuesta
        return JsonResponse({'status': 'error', 'message': 'Error desconocido.'}, status=500)

# vistas de cabezales
class CabezalListView(LoginRequiredMixin, TemplateView):
    template_name = 'cabezales/listar_cabezales.html'
    login_url = reverse_lazy('usuarios:login')


class CabezalDataView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def get(self, request, *args, **kwargs):
        cabezales = Cabezal.objects.annotate(
            numero_maquina=Concat(
                Value('Maquina-'), F('maquina__numero'), output_field=CharField()),
            planta_maquina=F('maquina__planta__nombre'),
        ).values()  # Elimina la anotación aquí
        cabezales_list = list(cabezales)
        return JsonResponse(cabezales_list, safe=False)



class CabezalCreateView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        nombre = request.POST.get('nombre').upper()  # Convertir a mayúsculas
        maquina_id = request.POST.get('maquina')

        if not (nombre and maquina_id):
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

        try:
            maquina = Maquina.objects.get(id=maquina_id)
            cabezal = Cabezal(nombre=nombre, maquina=maquina)
            cabezal.full_clean()  # Llamar clean para validaciones
            cabezal.save()
            return JsonResponse({'status': 'success', 'id': cabezal.id})
        except Maquina.DoesNotExist:
            return JsonResponse({'error': 'Máquina no encontrada.'}, status=404)
        except ValidationError as e:
            # Convertir los errores a un formato más legible sin nombres de campos
            errors = []
            for messages in e.message_dict.values():
                errors.extend(messages)
            return JsonResponse({'error': ' '.join(errors)}, status=400)




class CabezalUpdateView(LoginRequiredMixin, View):
    def post(self, request, id, *args, **kwargs):
        nombre = request.POST.get('nombre').upper()  # Convertir a mayúsculas
        maquina_id = request.POST.get('maquina')

        if not (nombre and maquina_id):
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

        try:
            maquina = Maquina.objects.get(id=maquina_id)
            cabezal = Cabezal.objects.get(pk=id)
            cabezal.nombre = nombre
            cabezal.maquina = maquina
            cabezal.full_clean()  # Llamar clean para validaciones
            cabezal.save()
            return JsonResponse({'status': 'success', 'id': cabezal.id})
        except Maquina.DoesNotExist:
            return JsonResponse({'error': 'Máquina no encontrada.'}, status=404)
        except Cabezal.DoesNotExist:
            return JsonResponse({'error': 'Cabezal no encontrado'}, status=404)
        except ValidationError as e:
            # Convertir los errores a un formato más legible sin nombres de campos
            errors = []
            for messages in e.message_dict.values():
                errors.extend(messages)
            return JsonResponse({'error': ' '.join(errors)}, status=400)



class CabezalDeleteView(LoginRequiredMixin, View):
    def delete(self, request, id, *args, **kwargs):
        try:
            cabezal = Cabezal.objects.get(pk=id)
            cabezal.delete()
            return JsonResponse({'status': 'success'})
        except Cabezal.DoesNotExist:
            return JsonResponse({'error': 'Cabezal no encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)


# vistas de plantas


class PlantaListView(LoginRequiredMixin, TemplateView):
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

# vistas de proveedores


# vistas de proveedores


class ProveedorListView(LoginRequiredMixin, TemplateView):
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

class ProveedorCreateView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def post(self, request, *args, **kwargs):
        data = request.POST
        nombre = data.get('nombre')
        telefono = data.get('telefono')
        correo = data.get('correo')
        planta_id = data.get('planta_id')

        if not (nombre and telefono and correo and planta_id):
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

        try:
            planta = Planta.objects.get(id=planta_id)
            proveedor = Proveedor.objects.create(
                nombre=nombre,
                telefono=telefono,
                correo=correo,
                planta=planta
            )
            return JsonResponse({'id': proveedor.id, 'nombre': proveedor.nombre})
        except Planta.DoesNotExist:
            return JsonResponse({'error': 'La planta seleccionada no existe.'}, status=400)
        except IntegrityError:
            return JsonResponse({'error': 'Error al crear el proveedor.'}, status=400)

        return JsonResponse({'error': 'Error desconocido.'}, status=500)

class ProveedorUpdateView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def post(self, request, pk, *args, **kwargs):
        data = request.POST
        nombre = data.get('nombre')
        telefono = data.get('telefono')
        correo = data.get('correo')
        planta_id = data.get('planta_id')

        if not (nombre  and telefono and correo and planta_id):
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

        try:
            proveedor = Proveedor.objects.get(pk=pk)
            planta = Planta.objects.get(id=planta_id)
            proveedor.nombre = nombre
            proveedor.telefono = telefono
            proveedor.correo = correo
            proveedor.planta = planta
            proveedor.save()
            return JsonResponse({'id': proveedor.id, 'nombre': proveedor.nombre})
        except Proveedor.DoesNotExist:
            return JsonResponse({'error': 'Proveedor no encontrado'}, status=404)
        except Planta.DoesNotExist:
            return JsonResponse({'error': 'La planta seleccionada no existe.'}, status=400)
        except IntegrityError:
            return JsonResponse({'error': 'Error al actualizar el proveedor.'}, status=400)

        return JsonResponse({'error': 'Error desconocido.'}, status=500)


class ProveedorDeleteView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def delete(self, request, pk, *args, **kwargs):
        try:
            proveedor = Proveedor.objects.get(pk=pk)
            proveedor.delete()
            return JsonResponse({'success': 'Proveedor eliminado con éxito'})
        except Proveedor.DoesNotExist:
            return JsonResponse({'error': 'Proveedor no encontrado'}, status=404)

        return JsonResponse({'error': 'Error desconocido.'}, status=500)



# vistas de silos
class SiloListView(LoginRequiredMixin, TemplateView):
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



# Vista de creación de silo

class SiloCreateView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def post(self, request, *args, **kwargs):
        numero = request.POST.get('numero')
        capacidad = request.POST.get('capacidad')
        producto_id = request.POST.get('producto_id')
        planta_id = request.POST.get('planta_id')

        if not numero or not capacidad or not producto_id or not planta_id:
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

        try:
            producto = get_object_or_404(Producto, id=producto_id)
            planta = get_object_or_404(Planta, id=planta_id)

            silo = Silo.objects.create(
                numero=numero,
                capacidad=capacidad,
                producto=producto,
                planta=planta
            )

            return JsonResponse({
                'success': True,
                'message': 'Silo creado con éxito',
                'id': silo.id,
                'numero': silo.numero,
                'capacidad': silo.capacidad,
                'nombre_producto': silo.producto.nombre,
                'nombre_planta': silo.planta.nombre
            })
        except IntegrityError as e:
            if 'UNIQUE constraint failed' in str(e):
                return JsonResponse({'error': 'El número del silo ya existe para esta planta. Por favor, elige otro número.'}, status=400)
            return JsonResponse({'error': f'Error al crear el silo: {str(e)}'}, status=400)

class SiloUpdateView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def get(self, request, *args, **kwargs):
        silo_id = kwargs.get('silo_id')
        try:
            silo = get_object_or_404(Silo, id=silo_id)
            response_data = {
                'id': silo.id,
                'numero': silo.numero,
                'capacidad': silo.capacidad,
                'producto_id': silo.producto.id,
                'planta_id': silo.planta.id
            }
            return JsonResponse(response_data)
        except Silo.DoesNotExist:
            return JsonResponse({'error': 'Silo no encontrado'}, status=404)

    def post(self, request, *args, **kwargs):
        silo_id = kwargs.get('silo_id')
        numero = request.POST.get('numero')
        capacidad = request.POST.get('capacidad')
        producto_id = request.POST.get('producto_id')
        planta_id = request.POST.get('planta_id')

        if not numero or not capacidad or not producto_id or not planta_id:
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

        try:
            silo = get_object_or_404(Silo, id=silo_id)
            producto = get_object_or_404(Producto, id=producto_id)
            planta = get_object_or_404(Planta, id=planta_id)

            # Validar que el número de silo es único en la planta, excluyendo el silo actual
            if Silo.objects.exclude(id=silo_id).filter(numero=numero, planta=planta).exists():
                return JsonResponse({'error': 'El número del silo ya existe en esta planta'}, status=400)

            silo.numero = numero
            silo.capacidad = capacidad
            silo.producto = producto
            silo.planta = planta
            silo.save()

            return JsonResponse({
                'success': True,
                'message': 'Silo actualizado con éxito',
                'id': silo.id,
                'numero': silo.numero,
                'capacidad': silo.capacidad,
                'nombre_producto': silo.producto.nombre,
                'nombre_planta': silo.planta.nombre
            })
        except IntegrityError:
            return JsonResponse({'error': 'Error al actualizar el silo. Es posible que el número ya exista.'}, status=400)

class SiloDeleteView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def post(self, request, *args, **kwargs):
        silo_id = kwargs.get('silo_id')

        try:
            silo = get_object_or_404(Silo, id=silo_id)
            silo.delete()

            return JsonResponse({'success': True})
        except Silo.DoesNotExist:
            return JsonResponse({'error': 'Silo no encontrado.'}, status=404)
        except IntegrityError:
            return JsonResponse({'error': 'Error al eliminar el silo.'}, status=400)




# vistas de turnos

class TurnoListView(LoginRequiredMixin, TemplateView):
    template_name = 'turnos/listar_turnos.html'
    login_url = reverse_lazy('usuarios:login')


class TurnoDataView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def get(self, request, *args, **kwargs):
        turnos = Turno.objects.values()  # Elimina la anotación aquí
        turnos_list = list(turnos)
        return JsonResponse(turnos_list, safe=False)


class TurnoCreateView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def post(self, request, *args, **kwargs):
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')
        estatus = request.POST.get('estatus') == 'true'  # Convertir el valor del checkbox a booleano

        if not nombre or not descripcion or not hora_inicio or not hora_fin:
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

        # Validar formato de hora
        try:
            hora_inicio = datetime.strptime(hora_inicio, '%H:%M').time()
            hora_fin = datetime.strptime(hora_fin, '%H:%M').time()
        except ValueError:
            return JsonResponse({'error': 'Formato de hora inválido. Use HH:MM'}, status=400)

        # Validar que el nombre del turno no exista
        if Turno.objects.filter(nombre=nombre).exists():
            return JsonResponse({'error': 'Ya existe un turno con ese nombre'}, status=400)

        # Crear el nuevo turno
        Turno.objects.create(
            nombre=nombre,
            descripcion=descripcion,
            hora_inicio=hora_inicio,
            hora_fin=hora_fin,
            estatus=estatus
        )

        return JsonResponse({'message': 'Turno creado con éxito'}, status=200)


class TurnoUpdateView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def post(self, request, pk, *args, **kwargs):
        turno = get_object_or_404(Turno, pk=pk)
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        hora_inicio = request.POST.get('hora_inicio')
        hora_fin = request.POST.get('hora_fin')
        estatus = request.POST.get('estatus') == 'true'  # Convertir el valor del checkbox a booleano

        if not nombre or not descripcion or not hora_inicio or not hora_fin:
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

        # Validar que el nombre del turno no exista para otros turnos
        if Turno.objects.exclude(pk=pk).filter(nombre=nombre).exists():
            return JsonResponse({'error': 'Ya existe un turno con ese nombre'}, status=400)

        # Actualizar el turno
        turno.nombre = nombre
        turno.descripcion = descripcion
        turno.hora_inicio = hora_inicio
        turno.hora_fin = hora_fin
        turno.estatus = estatus
        turno.save()

        return JsonResponse({'message': 'Turno actualizado con éxito'}, status=200)


class TurnoDeleteView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def delete(self, request, pk, *args, **kwargs):
        turno = get_object_or_404(Turno, pk=pk)
        turno.delete()
        return JsonResponse({'message': 'Turno eliminado con éxito'}, status=200)

# vistas para gestion de productos

class ProductoListView(LoginRequiredMixin, TemplateView):
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



class ProductoCreateView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def post(self, request, *args, **kwargs):
        data = request.POST
        nombre = data.get('nombre')
        tipo_producto_id = data.get('tipo_producto_id')

        if not (nombre and tipo_producto_id):
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

        try:
            tipo_producto = TipoProducto.objects.get(id=tipo_producto_id)
            producto = Producto.objects.create(
                nombre=nombre,
                tipo_producto=tipo_producto
            )
            return JsonResponse({
                'id': producto.id,
                'nombre': producto.nombre,
                'tipo_producto_nombre': tipo_producto.nombre  # Devolver esto si es necesario para el frontend
            })
        except IntegrityError:
            return JsonResponse({'error': 'Error al crear el producto.'}, status=400)
        except TipoProducto.DoesNotExist:
            return JsonResponse({'error': 'Tipo de producto no encontrado.'}, status=400)

class ProductoDeleteView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def delete(self, request, *args, **kwargs):
        producto_id = kwargs.get('producto_id')

        try:
            producto = get_object_or_404(Producto, id=producto_id)
            producto.delete()
            return JsonResponse({'mensaje': 'Producto eliminado con éxito'})
        except Producto.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado.'}, status=404)

class ProductoUpdateView(View):
    def post(self, request, *args, **kwargs):
        producto_id = kwargs.get('pk')  # Obtener el ID del producto de la URL
        nombre = request.POST.get('nombre')
        tipo_producto_id = request.POST.get('tipo_producto_id')

        # Validar que todos los campos requeridos estén presentes
        if not nombre or not tipo_producto_id:
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

        try:
            producto = get_object_or_404(Producto, id=producto_id)
            tipo_producto = get_object_or_404(TipoProducto, id=tipo_producto_id)

            producto.nombre = nombre
            producto.tipo_producto = tipo_producto
            producto.save()

            return JsonResponse({
                'id': producto.id,
                'nombre': producto.nombre,
                'nombre_tipo_producto': producto.tipo_producto.nombre
            })
        except IntegrityError:
            return JsonResponse({'error': 'Error al actualizar el producto.'}, status=400)
        except Producto.DoesNotExist:
            return JsonResponse({'error': 'Producto no encontrado.'}, status=404)
        except TipoProducto.DoesNotExist:
            return JsonResponse({'error': 'Tipo de producto no encontrado.'}, status=404)

class TipoProductoListView(LoginRequiredMixin, TemplateView):
    template_name = 'gestion_de_productos/listar_tipo_productos.html'
    login_url = reverse_lazy('usuarios:login')




class TipoProductoDataView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def get(self, request, *args, **kwargs):
        tipo_productos = TipoProducto.objects.values()  # Elimina la anotación aquí
        tipo_productos_list = list(tipo_productos)
        return JsonResponse(tipo_productos_list, safe=False)

class TipoProductoCreateView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def post(self, request, *args, **kwargs):
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')

        if not nombre or not descripcion:
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

        try:
            tipo_producto = TipoProducto.objects.create(nombre=nombre, descripcion=descripcion)
            return JsonResponse({
                'id': tipo_producto.id,
                'nombre': tipo_producto.nombre,
                'descripcion': tipo_producto.descripcion
            })
        except IntegrityError:
            return JsonResponse({'error': 'Error al crear el tipo de producto.'}, status=400)

class TipoProductoUpdateView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def post(self, request, *args, **kwargs):
        tipo_producto_id = kwargs.get('tipo_producto_id')
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')

        if not nombre or not descripcion:
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)

        try:
            tipo_producto = get_object_or_404(TipoProducto, id=tipo_producto_id)
            tipo_producto.nombre = nombre
            tipo_producto.descripcion = descripcion
            tipo_producto.save()

            return JsonResponse({
                'id': tipo_producto.id,
                'nombre': tipo_producto.nombre,
                'descripcion': tipo_producto.descripcion
            })
        except IntegrityError:
            return JsonResponse({'error': 'Error al actualizar el tipo de producto.'}, status=400)
        except TipoProducto.DoesNotExist:
            return JsonResponse({'error': 'Tipo de producto no encontrado.'}, status=404)

class TipoProductoDeleteView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')

    def post(self, request, *args, **kwargs):
        tipo_producto_id = kwargs.get('tipo_producto_id')

        try:
            tipo_producto = get_object_or_404(TipoProducto, id=tipo_producto_id)
            tipo_producto.delete()

            return JsonResponse({'success': True})
        except TipoProducto.DoesNotExist:
            return JsonResponse({'error': 'Tipo de producto no encontrado.'}, status=404)
        except IntegrityError:
            return JsonResponse({'error': 'Error al eliminar el tipo de producto.'}, status=400)


# vistas para rutas
class RutaListView(LoginRequiredMixin, TemplateView):
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