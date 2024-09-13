#Importaciones de modelos y formularios
from .models import *
from .forms import *
#Importaciones de vistas genéricas
from django.views.generic import TemplateView, DeleteView
from urllib import request
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views import generic 
from django.views import View
#Importaciones de redirecciones
from django.shortcuts import render, redirect, get_object_or_404
from django.urls  import reverse_lazy
#Importaciones de mensajes
from django.contrib import messages
#Otras importaciones
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic.edit import CreateView
from django.db import transaction
from usuarios.utils.mixins import GroupRequiredMixin

from usuarios.models import Usuario
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission #Importamos el modelo Permission



from django.views.generic import UpdateView
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.response import Response
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework import status
import json




# Create your views here.
class index(LoginRequiredMixin,TemplateView, PermissionRequiredMixin ):
    model = get_user_model()
    template_name = 'index.html'
    login_url = reverse_lazy('usuarios:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_usuarios'] = self.model.objects.exclude(is_staff=True).count()
        
        # Verifica si el usuario tiene el permiso directamente o a través de sus grupos
        permiso_nombre = 'usuario.add_usuario'
        tiene_permiso = self.request.user.has_perm(permiso_nombre) or \
                        self.request.user.groups.filter(permissions__codename=permiso_nombre.split('.')[1]).exists()
        context['puede_agregar_usuario'] = tiene_permiso
        return context



#Vistas aun en construcción    
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

#Vistas aun en construcción    

#Index de la aplicación
class index(LoginRequiredMixin,TemplateView, PermissionRequiredMixin):
    model = get_user_model()
    template_name = 'index.html'
    login_url = reverse_lazy('usuarios:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_usuarios'] = self.model.objects.exclude(is_staff=True).count()
        
        # Verifica si el usuario tiene el permiso directamente o a través de sus grupos
        permiso_nombre = 'usuario.add_usuario'
        tiene_permiso = self.request.user.has_perm(permiso_nombre) or \
                        self.request.user.groups.filter(permissions__codename=permiso_nombre.split('.')[1]).exists()
        context['puede_agregar_usuario'] = tiene_permiso
        return context
    

class LecheReconsSilosEncabView(generic.ListView):
    model = LecheReconsSilosEncab
    queryset = LecheReconsSilosEncab.objects.all()
    template_name = 'Leche_Reconstituida_Por_Silos_Encab/Leche_Reconstituida_Por_Silos_Encab_List.html'
    context_object_name = 'LecheReconsSilosEncab'
 


class LecheReconsSilosEncabCreate(View):
    success_url = reverse_lazy('laboratorio_control_calidad:Leche_Recons_Silos_Encab_List')

    def get(self, request, *args, **kwargs):
        encab_form = LecheReconsSilosEncabForm()
        silos_formset = LecheReconsSilosFormSet(queryset=LecheReconsSilos.objects.none())
        return render(request, 'Leche_Reconstituida_por_Silos_Encab/Leche_Reconstituida_Por_Silos_Encab_Create.html', {
            'encab_form': encab_form,
            'silos_formset': silos_formset,
        })

    def post(self, request, *args, **kwargs):
        encab_form = LecheReconsSilosEncabForm(request.POST)
        silos_formset = LecheReconsSilosFormSet(request.POST)

        if encab_form.is_valid():
            encab_instance = encab_form.save()
            silos_valid = True
            for form in silos_formset:
                if form.is_valid() and self._has_data(form.cleaned_data):
                    silo = form.save(commit=False)
                    silo.encabezado = encab_instance
                    silo.save()
                elif not form.is_valid() and self._has_data(form.cleaned_data):
                    silos_valid = False
                    break

            if silos_valid:
                return redirect(self.success_url)
            else:
                messages.error(request, f'Error en el formulario de Silos: {silos_formset.errors}')
        else:
            messages.error(request, f'Error en el formulario de Encab: {encab_form.errors}')

        return render(request, 'Leche_Reconstituida_por_Silos_Encab/Leche_Reconstituida_Por_Silos_Encab_Create.html', {
            'encab_form': encab_form,
            'silos_formset': silos_formset,
        })

    def _has_data(self, cleaned_data):
        # Verificar si el formulario tiene datos significativos
        default_datetime = timezone.now()
        for key, value in cleaned_data.items():
            if key == 'fecha_Hora' and value == default_datetime:
                continue
            if key != 'id' and value not in (None, '', 0.0, 0):
                return True
        return False


class LecheReconsSilosEncabUpdate(View):
    success_url = reverse_lazy('laboratorio_control_calidad:Leche_Recons_Silos_Encab_List')

    def get(self, request, *args, **kwargs):
        encab = get_object_or_404(LecheReconsSilosEncab, pk=kwargs['pk'])
        encab_form = LecheReconsSilosEncabForm(instance=encab)
        silos_formset = LecheReconsSilosFormSet(instance=encab)
        return render(request, 'Leche_Reconstituida_por_Silos_Encab/Leche_Reconstituida_Por_Silos_Encab_Create.html', {
            'encab_form': encab_form,
            'silos_formset': silos_formset,
        })

    def post(self, request, *args, **kwargs):
        encab = get_object_or_404(LecheReconsSilosEncab, pk=kwargs['pk'])
        encab_form = LecheReconsSilosEncabForm(request.POST, instance=encab)
        silos_formset = LecheReconsSilosFormSet(request.POST, instance=encab)
        if encab_form.is_valid() and silos_formset.is_valid():
            encab = encab_form.save()
            silos_formset.save()  # Guarda el formset con la instancia adecuada
            return redirect(self.success_url)
        else:
            if not encab_form.is_valid():
                messages.error(request, f'Error en el formulario de Encabezado: {encab_form.errors}')
            if not silos_formset.is_valid():
                messages.error(request, f'Error en el formulario de Silos: {silos_formset.errors}')

        return render(request, 'Leche_Reconstituida_por_Silos_Encab/Leche_Reconstituida_Por_Silos_Encab_Create.html', {
            'encab_form': encab_form,
            'silos_formset': silos_formset,
        })

   

class LecheReconsSilosEncabDelete(DeleteView):
    model = LecheReconsSilosEncab
    template_name = 'Leche_Reconstituida_Por_Silos_Encab/Leche_Reconstituida_Por_Silos_Encab_Delete.html'
    context_object_name = 'LecheReconsSilosEncab'
    success_url = reverse_lazy('laboratorio_control_calidad:Leche_Recons_Silos_Encab_List')
    
 
class TerminadoEncabView(generic.ListView):
    model = terminadoEncab
    queryset = terminadoEncab.objects.all()
    template_name = 'pterminado_encab_list.html'
    context_object_name = 'terminadoEncab'

class TerminadoEncabCreate(View):
    success_url = reverse_lazy('laboratorio_control_calidad:TerminadoList')

#=========================[Start] Leche Reconstituida por silos  [Start]==============================#

class LecheReconsSilosView(generic.ListView):
    model = LecheReconsSilosEncab
    queryset = LecheReconsSilosEncab.objects.all()
    template_name = 'Leche_Reconstituida_Por_Silos/Leche_Recons_Silos_List.html'
    context_object_name = 'LecheReconsSilosEncab'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['encab'] = LecheReconsSilosEncabForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = LecheReconsSilosEncabForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('laboratorio_control_calidad:Leche_Recons_Silos_List')
        else:
            print("Form errors:", form.errors)  # Agrega esta línea para ver los errores del formulario
        return self.get(request, *args, **kwargs)

    
class LecheReconsSilosUpdate(generic.UpdateView):
    model = LecheReconsSilosEncab
    template_name = 'Leche_Reconstituida_Por_Silos/Leche_Recons_Silos_Create.html'
    context_object_name = 'LecheReconsSilosEncab'
    form_class = LecheReconsSilosEncabForm
    success_url = reverse_lazy('laboratorio_control_calidad:Leche_Recons_Silos_List')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        encab_object = self.get_object()
        context['silos'] = LecheReconsSilos.objects.filter(encabezado=encab_object)

        # Obtener el ID del silo desde los parámetros GET para edición
        silo_id = self.request.GET.get('silo_id')
        if silo_id:
            try:
                nuevo_form = LecheReconsSilosForm(instance=LecheReconsSilos.objects.get(id=silo_id))
                context['edit_mode'] = True
            except LecheReconsSilos.DoesNotExist:
                # Si el ID no existe, inicializar el formulario para un nuevo registro
                nuevo_form = LecheReconsSilosForm(initial={'encabezado': encab_object})
                context['edit_mode'] = False
        else:
            nuevo_form = LecheReconsSilosForm(initial={'encabezado': encab_object})
            context['edit_mode'] = False

        # Desactivar edición del encabezado
        nuevo_form.fields['encabezado'].widget.attrs['readonly'] = True
        context['form'] = self.get_form()
        context['nuevo_form'] = nuevo_form
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        silo_id = request.POST.get('silo_id')

        # Asegurarse de que el formulario esté correctamente ligado a la instancia existente
        if silo_id and silo_id.isdigit():
            try:
                silo_instance = LecheReconsSilos.objects.get(id=silo_id)
                nuevo_form = LecheReconsSilosForm(request.POST, instance=silo_instance)
            except LecheReconsSilos.DoesNotExist:
                nuevo_form = LecheReconsSilosForm(request.POST)
        else:
            nuevo_form = LecheReconsSilosForm(request.POST)

        # Guardar el formulario de encabezado si se presionó su botón de guardar
        if 'submit-encab-form' in request.POST and form.is_valid():
            form.save()
            return redirect(self.success_url)

        # Guardar o actualizar el formulario de silo si se presionó su botón de guardar
        if 'submit-nuevo-form' in request.POST and nuevo_form.is_valid():
            nuevo_form.save()
            return redirect(request.path)

        # En caso de errores, renderizar los formularios con los datos ya ingresados
        context = self.get_context_data()
        context['form'] = form
        context['nuevo_form'] = nuevo_form
        return self.render_to_response(context)



class LecheReconsSilosDelete(DeleteView):
    model = LecheReconsSilosEncab
    template_name = 'Leche_Reconstituida_Por_Silos/Leche_Recons_Silos_Delete.html'
    context_object_name = 'LecheReconsSilosEncab'
    success_url = reverse_lazy('Leche_Recons_Silos_List')

class LecheReconsSilosDeleteSilo(DeleteView):
    model = LecheReconsSilos
    template_name = 'Leche_Reconstituida_Por_Silos/Leche_Recons_Silos_Delete_Silo.html'
    context_object_name = 'LecheReconsSilos'
    success_url = reverse_lazy('laboratorio_control_calidad:Leche_Recons_Silos_List')
    
 

#==========================[End] Leche Reconstituida por silos  [End]==============================#


class TerminadoEncabView(generic.ListView):
    model = terminadoEncab
    queryset = terminadoEncab.objects.all()
    template_name = 'producto_terminado/pterminado_encab_list.html'
    context_object_name = 'terminadoEncab'

class TerminadoEncabCreate(View):
    success_url = reverse_lazy('laboratorio_control_calidad:TerminadoList')

    def get(self, request, *args, **kwargs):
        encab_form = TerminadoEncabForm()
        terminado_formset = TerminadoFormSet(queryset=producto_terminado.objects.none())
        return render(request, 'producto_terminado/producto_terminado.html', {
            'encab_form': encab_form,
            'terminado_formset': terminado_formset,
        })

    def post(self, request, *args, **kwargs):
        encab_form = TerminadoEncabForm(request.POST)
        terminado_formset = TerminadoFormSet(request.POST)

        if encab_form.is_valid():
            encab_instance = encab_form.save()
            valid_forms = True

            for form in terminado_formset:
                # Verificar si el formulario está vacío (todos los campos vacíos)
                if not any(form.data.get(form.add_prefix(field)) for field in form.fields):
                    continue

                # Validar y guardar formularios no vacíos
                if form.is_valid():
                    terminado = form.save(commit=False)
                    terminado.encabezado = encab_instance
                    terminado.save()
                else:
                    valid_forms = False
                    break

            if valid_forms:
                return redirect(self.success_url)
        
        # Si hay algún error, también redirigir (esto incluye el caso donde encab_form no es válido)
        return redirect(self.success_url)
    
class TerminadoEncabUpdate(View):
    success_url = reverse_lazy('laboratorio_control_calidad:TerminadoList')

    def get(self, request, *args, **kwargs):
        encab = get_object_or_404(terminadoEncab, pk=kwargs['pk'])
        encab_form = TerminadoEncabForm(instance=encab)
        terminado_formset = TerminadoFormSet(instance=encab)
        return render(request, 'producto_terminado/producto_terminado.html', {
            'encab_form': encab_form,
            'terminado_formset': terminado_formset,
        })

    def post(self, request, *args, **kwargs):
        encab = get_object_or_404(terminadoEncab, pk=kwargs['pk'])
        encab_form = TerminadoEncabForm(request.POST, instance=encab)
        terminado_formset = TerminadoFormSet(request.POST, instance=encab)

        # Validar y guardar los formularios
        if encab_form.is_valid():
            encab_form.save()

        # Guardar formularios válidos del formset
        valid_forms = True
        for form in terminado_formset:
            # Verificar si el formulario está vacío (todos los campos vacíos)
            if not any(form.data.get(form.add_prefix(field)) for field in form.fields):
                continue

            if form.is_valid():
                form.save()
            else:
                valid_forms = False

        # Manejo de errores
        if not encab_form.is_valid() or not valid_forms:
             return redirect(self.success_url)

class TerminadoDelete(generic.DeleteView):
    model = terminadoEncab
    template_name = 'producto_terminado/terminadoDelete.html'
    context_object_name = 'terminado'
    success_url = reverse_lazy('laboratorio_control_calidad:pt_encabView')
    
class permisos(generic.UpdateView):
    model = terminadoEncab
    form_class = permisosForm
    template_name = "producto_terminado/modificar.html"
    success_url = reverse_lazy('laboratorio_control_calidad:TerminadoList')
    login_url = reverse_lazy('usuarios:login')

# Producto Terminado 2.0 ENCABEZADO--------------------------------
class EncabView(generic.ListView):
    model = terminadoEncab
    queryset = terminadoEncab.objects.all()
    template_name = 'producto_terminado2.0/EncabList.html'
    context_object_name = 'encab'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TerminadoEncabForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = TerminadoEncabForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('laboratorio_control_calidad:pt_encabView')
        else:
            print("Form errors:", form.errors)  # Agrega esta línea para ver los errores del formulario
        return self.get(request, *args, **kwargs)

class EncabCreate(generic.CreateView):
    model = terminadoEncab
    template_name = 'Leche_Reconstituida_Por_Silos/encabCreate.html'
    context_object_name = 'encab'
    form_class = TerminadoEncabForm
    success_url = reverse_lazy('laboratorio_control_calidad:pt_encabView')
    


class EncabUpdate(generic.UpdateView):
    model = terminadoEncab
    template_name = 'producto_terminado2.0/encabCreate.html'
    context_object_name = 'Encab'
    form_class = TerminadoEncabForm
    success_url = reverse_lazy('laboratorio_control_calidad:pt_encabView')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        encab_object = self.get_object()
        context['term'] = producto_terminado.objects.filter(encabezado=encab_object)

        # Si se recibe un ID en el GET, se está editando un registro; de lo contrario, es un nuevo registro.
        term_id = self.request.GET.get('term_id')
        if term_id:
            try:
                term_instance = producto_terminado.objects.get(id=term_id)
                nuevo_form = TerminadoForm(instance=term_instance)
                context['edit_mode'] = True
            except producto_terminado.DoesNotExist:
                nuevo_form = TerminadoForm(initial={'encabezado': encab_object})
                context['edit_mode'] = False
        else:
            nuevo_form = TerminadoForm(initial={'encabezado': encab_object})
            context['edit_mode'] = False

        nuevo_form.fields['encabezado'].widget.attrs['readonly'] = True
        context['form'] = self.get_form()
        context['nuevo_form'] = nuevo_form
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        term_id = request.POST.get('term_id')

        # Crear nuevo formulario de producto_terminado dependiendo de si es una edición o creación
        if term_id and term_id.isdigit():
            try:
                term_instance = producto_terminado.objects.get(id=term_id)
                nuevo_form = TerminadoForm(request.POST, instance=term_instance)
            except producto_terminado.DoesNotExist:
                nuevo_form = TerminadoForm(request.POST)
        else:
            nuevo_form = TerminadoForm(request.POST)

        # Guardar el formulario de encabezado si se presionó su botón de guardar
        if 'submit-encab-form' in request.POST and form.is_valid():
            form.save()
            return redirect(self.success_url)

        # Guardar el formulario de nuevo producto_terminado si se presionó su botón de guardar
        if 'submit-nuevo-form' in request.POST and nuevo_form.is_valid():
            nuevo_form.save()
            return redirect(request.path)

        # En caso de errores, renderizar los formularios con los datos ya ingresados
        context = self.get_context_data()
        context['form'] = form
        context['nuevo_form'] = nuevo_form
        return self.render_to_response(context)




# Producto Terminado 2.0 ---------------------------------------

class TerminadoView(generic.ListView): 
    model =  producto_terminado
    queryset = producto_terminado.objects.all()
    template_name = 'producto_terminado2.0/TerminadoView.html'
    context_object_name = 'term'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TerminadoForm()
        context['encab'] = TerminadoEncabForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = TerminadoForm(request.POST)
        formencab = TerminadoEncabForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('laboratorio_control_calidad:pt_View')
        else:
            print("Form errors:", form.errors)  # Agrega esta línea para ver los errores del formulario
        return self.get(request, *args, **kwargs)
    
        if formencab.is_valid():
            formencab.save()
            return redirect('laboratorio_control_calidad:pt_View')
        else:
            print("Form errors:", formencab.errors)  # Agrega esta línea para ver los errores del formulario
        return self.get(request, *args, **kwargs)


class TerminadoCreate(generic.CreateView):
    model = producto_terminado
    template_name = 'producto_terminado2.0/TerminadoCreate.html'
    context_object_name = 'term'
    form_class = TerminadoForm
    success_url = reverse_lazy("laboratorio_control_calidad:TerminadoList")

class TerminadoUpdate(generic.UpdateView):
    model = producto_terminado
    template_name = 'producto_terminado2.0/TerminadoCreate.html'
    context_object_name = 'term'
    form_class = TerminadoForm
    success_url = reverse_lazy('laboratorio_control_calidad:TerminadoList')

class PTerminadoDelete(generic.DeleteView):
    model = producto_terminado
    template_name = 'producto_terminado2.0/pterminadoDelete.html'
    context_object_name = 'term'
    success_url = reverse_lazy('laboratorio_control_calidad:pt_encabView')
    
   

    
#Calidad Microbiológica ---------------------------------------

@api_view(['GET'])
def encabezados_list(request):
    encabezados = CalidadMicrobiologicaEncabezado.objects.all()
    serializer = CalidadMicrobiologicaEncabezadoSerializer(encabezados, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def planta_list(request):
    plantas = Planta.objects.all()
    serializer = PlantaSerializer(plantas, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def producto_list(request):
    productos = Producto.objects.all()
    serializer = ProductoSerializer(productos, many=True)
    return Response(serializer.data)

class CalidadMicrobiologicaView(LoginRequiredMixin, TemplateView):
    template_name = 'CalidadMicrobiologica/calidad_microbiologica.html'
    login_url = reverse_lazy('usuarios:login')

    def post(self, request, *args, **kwargs):
        # Manejar la creación de un nuevo encabezado
        if 'crear_encabezado' in request.POST:
            folio = request.POST.get('folio')
            if folio:  # Verifica que folio no esté vacío
                CalidadMicrobiologicaEncabezado.objects.create(
                    folio=folio
                )
            return redirect('laboratorio_control_calidad:calidad_microbiologica')

        # Manejar la eliminación de un encabezado
        elif 'delete_encabezado' in request.POST:
            encabezado_id = request.POST.get('encabezado_id')
            encabezado = get_object_or_404(CalidadMicrobiologicaEncabezado, id=encabezado_id)
            encabezado.delete()
            return redirect('laboratorio_control_calidad:calidad_microbiologica')

        return self.get(request, *args, **kwargs)
    

class CalidadMicrobiologicaEncabezadoUpdateView(UpdateView):
    model = CalidadMicrobiologicaEncabezado
    fields = ['folio', 'observaciones']
    template_name = 'calidad_microbiologica_encabezado_form.html'
    success_url = reverse_lazy('laboratorio_control_calidad:calidad_microbiologica')  # Redirige a la vista de calidad microbiológica

    def form_valid(self, form):
        # Puedes agregar lógica adicional aquí si es necesario
        return super().form_valid(form)

    
class CalidadMicrobiologicaDeleteEncabezadoView(View):
    def delete(self, request, *args, **kwargs):
        encabezado_id = kwargs.get('encabezado_id')
        encabezado = get_object_or_404(CalidadMicrobiologicaEncabezado, id=encabezado_id)
        encabezado.delete()
        return JsonResponse({'status': 'success'})
    
class CalidadMicrobiologicaDetalleView(View):
    def get(self, request, encabezado_id):
        encabezado = get_object_or_404(CalidadMicrobiologicaEncabezado, id=encabezado_id)
        calidad_microbiologica = CalidadMicrobiologica.objects.filter(encabezado=encabezado)
        context = {
            'encabezado': encabezado,
            'calidad_microbiologica': calidad_microbiologica
        }
        return render(request, 'CalidadMicrobiologica/calidad_microbiologica_detalles.html', context)
    
@csrf_exempt
def add_calidad_microbiologica(request, encabezado_id):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            # Obtiene los datos del cuerpo de la solicitud
            fechaHora = data.get('fechaHora')
            planta = data.get('planta')
            producto = data.get('producto')
            organismos_coliformes = data.get('organismos_coliformes')
            encabezado_id = data.get('encabezado_id')

            # Verifica que todos los campos requeridos estén presentes
            if not all([fechaHora, planta, producto, organismos_coliformes, encabezado_id]):
                return JsonResponse({'success': False, 'error': 'Missing required fields'}, status=400)

            # Procesa y guarda los datos en la base de datos
            # Aquí debes agregar la lógica para guardar los datos en la base de datos
            # Ejemplo:
            from .models import CalidadMicrobiologica

            # Asumiendo que planta_id y producto_id son IDs que se deben convertir
            try:
                from .models import Planta, Producto
                planta_instance = Planta.objects.get(id=planta)
                producto_instance = Producto.objects.get(id=producto)
            except Planta.DoesNotExist or Producto.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Invalid planta or producto ID'}, status=400)

            # Crea una nueva instancia del modelo
            calidad = CalidadMicrobiologica(
                fechaHora=fechaHora,
                planta=planta_instance,
                producto=producto_instance,
                organismos_coliformes=organismos_coliformes,
                encabezado_id=encabezado_id
            )
            calidad.save()

            return JsonResponse({'success': True})

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

@api_view(['GET'])
def calidad_microbiologica_list(request):
    encabezado_id = request.query_params.get('encabezado_id', None)
    
    if encabezado_id is None:
        return Response({'error': 'El parámetro encabezado_id es requerido'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        encabezado_id = int(encabezado_id)
    except ValueError:
        return Response({'error': 'ID de encabezado inválido'}, status=status.HTTP_400_BAD_REQUEST)
    
    queryset = CalidadMicrobiologica.objects.filter(encabezado_id=encabezado_id)
    
    if not queryset.exists():
        return Response({'error': 'No se encontraron registros con el encabezado_id proporcionado'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CalidadMicrobiologicaSerializer(queryset, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
def calidad_microbiologica_delete(request, pk):
    try:
        registro = CalidadMicrobiologica.objects.get(pk=pk)
    except CalidadMicrobiologica.DoesNotExist:
        return Response({'error': 'Registro no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    registro.delete()
    return Response({'success': True})

@api_view(['GET'])
def calidad_microbiologica_edit(request, pk):
    try:
        registro = CalidadMicrobiologica.objects.get(pk=pk)
    except CalidadMicrobiologica.DoesNotExist:
        return Response({'error': 'Registro no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CalidadMicrobiologicaSerializer(registro)
    return Response(serializer.data)

@api_view(['POST'])
def calidad_microbiologica_update(request):
    pk = request.data.get('id')
    try:
        registro = CalidadMicrobiologica.objects.get(pk=pk)
    except CalidadMicrobiologica.DoesNotExist:
        return Response({'error': 'Registro no encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = CalidadMicrobiologicaSerializer(registro, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'success': True})
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#Calidad Microbiológica ---------------------------------------

#Juan Carlos M. Peso Bruto, Peso Envase Vacio

# START--PRUEBAS VISTA PESO NETO  -----------------------------------------------------------|

class MostrarPesosView(LoginRequiredMixin, TemplateView):
    # model = Pesobruto  #borrar locomentado si no hay errores
    # queryset = Pesobruto.objects.all()
    template_name = 'pesonetor49_list.html'
    login_url = reverse_lazy('usuarios:login')
    # context_object_name = 'pesos'       
# END--PRUEBAS VISTA PESO NETO  -----------------------------------------------------------|    

# START--PRUEBAS VISTA PESO NETO  ---------------------------------------------------------|
#DENSIDAD(
class Densidadr49ListView(generic.ListView):
     model = Densidadpt
     queryset = Densidadpt.objects.all ()
     template_name = 'crud_VolumenNetoR49/densidad_List.html'
     context_object_name = 'densidadr49'

class Densidadr49CreateView(TemplateView):
    template_name = 'crud_VolumenNetoR49/densidad_Create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = DensidadptForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = DensidadptForm(request.POST)
        if form.is_valid():
            densidad = form.save()
            # Aquí capturas el pk del objeto recién guardado o relacionado
            return HttpResponseRedirect(reverse_lazy('laboratorio_control_calidad:encabezador49_update', kwargs={'pk': densidad.pk}))
        else:
            return self.render_to_response(self.get_context_data(form=form))
               
class Densidadr49UpdateView(generic.UpdateView):
    model = Densidadpt
    template_name = 'crud_VolumenNetoR49/densidad_Create.html' 
    form_class = DensidadptForm
    success_url = reverse_lazy('laboratorio_control_calidad:encabezador49_list')
    context_object_name = 'densidadr49'

class Densidadr49DeleteView(generic.DeleteView):
    model = Densidadpt
    template_name = 'crud_VolumenNetoR49/densidad_Delete.html'
    context_object_name = 'densidadr49'
    success_url = reverse_lazy('laboratorio_control_calidad:encabezador49_list')
#)

#PESO BRUTO (
class PesoBrutor49ListView(generic.ListView):
     model = Pesobruto
     queryset = Pesobruto.objects.all ()
     template_name = 'crud_VolumenNetoR49/pesoBruto_List.html'
     context_object_name = 'pesoBrutor49'

class PesoBrutor49CreateView(generic.CreateView):
    model = Pesobruto
    template_name = 'crud_VolumenNetoR49/pesoBruto_Create.html'
    context_object_name = 'pesoBrutor49'
    form_class = PesobrutoForm
    success_url = reverse_lazy("laboratorio_control_calidad:encabezador49_create")

class PesoBrutor49UpdateView(generic.UpdateView):
    model = Pesobruto
    template_name = 'crud_VolumenNetoR49/pesoBruto_Create.html' 
    form_class = PesobrutoForm
    success_url = reverse_lazy('laboratorio_control_calidad:encabezador49_list')
    context_object_name = 'pesoBrutor49'

class PesoBrutor49DeleteView(generic.DeleteView):
    model = Pesobruto
    template_name = 'crud_VolumenNetoR49/pesoBruto_Delete.html'
    context_object_name = 'pesoBrutor49'
    success_url = reverse_lazy('laboratorio_control_calidad:encabezador49_list')
#)

#PESO ENVASE VACIO (
class PesoEnvVacior49ListView(generic.ListView):
     model = Pesoenvvacio
     queryset = Pesoenvvacio.objects.all ()
     template_name = 'crud_VolumenNetoR49/pesoEnvVacio_List.html'
     context_object_name = 'pesoEnvVacior49'

class PesoEnvVacior49CreateView(generic.CreateView):
    model = Pesoenvvacio
    template_name = 'crud_VolumenNetoR49/pesoEnvVacio_Create.html'
    context_object_name = 'pesoEnvVacior49'
    form_class = PesoenvvacioForm
    success_url = reverse_lazy("laboratorio_control_calidad:encabezador49_update")

class PesoEnvVacior49UpdateView(generic.UpdateView):
    model = Pesoenvvacio
    template_name = 'crud_VolumenNetoR49/pesoEnvVacio_Create.html' 
    form_class = PesoenvvacioForm
    success_url = reverse_lazy('laboratorio_control_calidad:encabezador49_list')
    context_object_name = 'pesoEnvVacior49'

class PesoEnvVacior49DeleteView(generic.DeleteView):
    model = Pesoenvvacio
    template_name = 'crud_VolumenNetoR49/pesoEnvVacio_Delete.html'
    context_object_name = 'pesoEnvVacior49'
    success_url = reverse_lazy('laboratorio_control_calidad:encabezador49_list')
#)

#ENCABEZADO (
class EncabR49ListView(generic.ListView):
     model = EncabR49V2
     queryset = EncabR49V2.objects.all ()
     template_name = 'encabezador49V2_List.html'
     context_object_name = 'EncabR49'

     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['encab'] = EncabR49V2Form()
        return context
     
     def post(self, request, *args, **kwargs):
        form = EncabR49V2Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('laboratorio_control_calidad:encabezador49_list')
        else:
            print("Form errors:", form.errors)  # Agrega esta línea para ver los errores del formulario
        return self.get(request, *args, **kwargs)

class EncabR49UpdateView(generic.UpdateView):
    model = EncabR49V2
    template_name = 'encabezador49V2_Create.html'
    form_class = EncabR49V2Form
    success_url = reverse_lazy('laboratorio_control_calidad:encabezador49_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        encab_object = self.get_object()
        
        # Filtrar los datos relacionados al encabezado actual
        context['datosPesoBruto'] = Pesobruto.objects.filter(encabezado=encab_object)
        context['datosDensidad'] = Densidadpt.objects.filter(encabezado=encab_object)
        context['datosPesoEnvVacio'] = Pesoenvvacio.objects.filter(encabezado=encab_object)
        
        # Manejar los formularios de forma dinámica
        context['form_peso_bruto'] = self._get_related_form(Pesobruto, PesobrutoForm, 'peso_bruto_id', encab_object)
        context['form_densidad'] = self._get_related_form(Densidadpt, DensidadptForm, 'densidad_id', encab_object)
        context['form_pesoEnvVacio'] = self._get_related_form(Pesoenvvacio, PesoenvvacioForm, 'pesoEnvVacio_id', encab_object)

        context['form'] = self.get_form()  # Formulario principal

        context['edit_mode'] = bool(self.request.GET.get('peso_bruto_id') or self.request.GET.get('densidad_id') or self.request.GET.get('pesoEnvVacio_id'))

        return context

    def _get_related_form(self, model, form_class, param_name, encab_object):
        """Helper to generate form for related models."""
        instance_id = self.request.GET.get(param_name)
        if instance_id:
            try:
                return form_class(instance=model.objects.get(id=instance_id))
            except model.DoesNotExist:
                return form_class(initial={'encabezado': encab_object})
        else:
            return form_class(initial={'encabezado': encab_object})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()

        # Obtener formularios relacionados
        form_peso_bruto = self._handle_related_form_post(Pesobruto, PesobrutoForm, 'peso_bruto_id')
        form_densidad = self._handle_related_form_post(Densidadpt, DensidadptForm, 'densidad_id')
        form_pesoEnvVacio = self._handle_related_form_post(Pesoenvvacio, PesoenvvacioForm, 'pesoEnvVacio_id')

        # Guardar el formulario principal si se presionó su botón de guardar
        if 'submit-encab-form' in request.POST and form.is_valid():
            form.save()
            return redirect(self.success_url)

        # Guardar o actualizar los formularios relacionados
        if 'submit-peso-bruto-form' in request.POST and form_peso_bruto.is_valid():
            form_peso_bruto.save()
            return redirect(request.path)

        if 'submit-densidad-form' in request.POST and form_densidad.is_valid():
            form_densidad.save()
            return redirect(request.path)

        if 'submit-pesoEnvVacio-form' in request.POST and form_pesoEnvVacio.is_valid():
            form_pesoEnvVacio.save()
            return redirect(request.path)

        # En caso de errores, renderizar los formularios con los datos ya ingresados
        context = self.get_context_data()
        context['form'] = form
        context['form_peso_bruto'] = form_peso_bruto
        context['form_densidad'] = form_densidad
        context['form_pesoEnvVacio'] = form_pesoEnvVacio
        return self.render_to_response(context)

    def _handle_related_form_post(self, model, form_class, param_name):
        """Helper to handle POST for related models."""
        instance_id = self.request.POST.get(param_name)
        if instance_id and instance_id.isdigit():
            try:
                instance = model.objects.get(id=instance_id)
                return form_class(self.request.POST, instance=instance)
            except model.DoesNotExist:
                return form_class(self.request.POST)
        else:
            return form_class(self.request.POST)

class EncabR49DeleteView(generic.DeleteView):
    model = EncabR49V2
    template_name = 'encabezador49V2_Delete.html'
    context_object_name = 'EncabR49'
    success_url = reverse_lazy('laboratorio_control_calidad:encabezador49_list')
#)
# END--PRUEBAS VISTA PESO NETO  -----------------------------------------------------------|    

#
class TerminadoEncabUpdate(View):
    success_url = reverse_lazy('laboratorio_control_calidad:TerminadoList')

    def get(self, request, *args, **kwargs):
        encab = get_object_or_404(terminadoEncab, pk=kwargs['pk'])
        encab_form = TerminadoEncabForm(instance=encab)
        terminado_formset = TerminadoFormSet(instance=encab)
        return render(request, 'producto_terminado.html', {
            'encab_form': encab_form,
            'terminado_formset': terminado_formset,
        })

    def post(self, request, *args, **kwargs):
        encab = get_object_or_404(terminadoEncab, pk=kwargs['pk'])
        encab_form = TerminadoEncabForm(request.POST, instance=encab)
        terminado_formset = TerminadoFormSet(request.POST, instance=encab)

        # Validar y guardar los formularios
        if encab_form.is_valid():
            encab_form.save()

        # Guardar formularios válidos del formset
        valid_forms = True
        for form in terminado_formset:
            # Verificar si el formulario está vacío (todos los campos vacíos)
            if not any(form.data.get(form.add_prefix(field)) for field in form.fields):
                continue

            if form.is_valid():
                form.save()
            else:
                valid_forms = False

        # Manejo de errores
        if not encab_form.is_valid() or not valid_forms:
             return redirect(self.success_url)
        
#Fin Juan Carlos M. Peso Bruto, Peso Envase Vacio