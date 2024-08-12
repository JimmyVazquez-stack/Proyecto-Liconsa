from urllib import request
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views import generic 
from django.urls  import reverse_lazy
from django.views import View
from .models import *
from .forms import *
from django.contrib import messages
from django.views.generic.edit import CreateView
from django.db import transaction
from usuarios.utils.mixins import GroupRequiredMixin

from usuarios.models import Usuario
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission #Importamos el modelo Permission



from django.views.generic import DetailView


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



#=========================[Start] Leche Reconstituida por silos encab [Start]==============================#


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
    
 

#==========================[End] Leche Reconstituida por silos encab [End]==============================#

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
    
   

    
