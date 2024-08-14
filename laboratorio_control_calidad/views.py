#Importaciones de modelos y formularios
from django.shortcuts import render
from .models import *
from .forms import *
#Importaciones de vistas genéricas
from django.views.generic import TemplateView, DeleteView, FormView
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

#CRUD FormatoR49 Juan Carlos M.



class densidadr49_list(generic.ListView):
    model = Densidadpt
    queryset = Densidadpt.objects.all ()
    template_name = 'crud_VolumenNetoR49/densidad_List.html'
    context_object_name = 'densidadr49'

class densidadr49_create(generic.CreateView):
    model = Densidadpt
    template_name = 'crud_VolumenNetoR49/densidad_Create.html'
    context_object_name = 'densidadr49'
    form_class = DensidadptForm
    success_url = reverse_lazy("laboratorio_control_calidad:densidadr49_list")

class densidadr49_update(generic.UpdateView):
    model = Densidadpt
    template_name = 'crud_VolumenNetoR49/densidad_Create.html' 
    form_class = DensidadptForm
    success_url = reverse_lazy('laboratorio_control_calidad:encabezador49_create')
    context_object_name = 'densidadr49'

class densidadr49_delete(generic.DeleteView):
    model = Densidadpt
    template_name = 'crud_VolumenNetoR49/densidad_Delete.html'
    context_object_name = 'densidadr49'
    success_url = reverse_lazy('laboratorio_control_calidad:encabezador49_create')


### complementarias a formato R49 PESO ENVASE VACIO# 
class pesoenvvacior49_list(generic.ListView):
    model = Pesoenvvacio
    queryset = Pesoenvvacio.objects.all ()
    template_name = 'crud_VolumenNetoR49/pesoEnvVacio_List.html'
    context_object_name = 'pesoenvvacior49'

class pesoenvvacior49_create(generic.CreateView):
    model = Pesoenvvacio
    template_name = 'crud_VolumenNetoR49/pesoEnvVacio_Create.html'
    context_object_name = 'pesoenvvacior49'
    form_class = PesoenvvacioForm
    success_url = reverse_lazy('laboratorio_control_calidad:encabezador49_create')

class pesoenvvacior49_update(generic.UpdateView):
    model = Pesoenvvacio
    template_name = 'crud_VolumenNetoR49/pesoEnvVacio_Create.html' 
    form_class = PesoenvvacioForm
    success_url = reverse_lazy('laboratorio_control_calidad:encabezador49_create')
    context_object_name = 'pesoenvvacior49'

class pesoenvvacior49_delete(generic.DeleteView):
    model = Pesoenvvacio
    template_name = 'crud_VolumenNetoR49/pesoEnvVacio_Delete.html'
    context_object_name = 'densidadr49'
    success_url = reverse_lazy('laboratorio_control_calidad:pesoenvvacior49_list')

### complementarias a formato R49 PESO BRUTO
class pesobrutor49_list(generic.ListView):
    model = Pesobruto
    queryset = Pesobruto.objects.all ()
    template_name = 'crud_VolumenNetoR49/pesoBruto_List.html'
    context_object_name = 'pesobrutor49'

class pesobrutor49_create(generic.CreateView):
    model = Pesobruto
    template_name = 'crud_VolumenNetoR49/pesoBruto_Create.html'
    context_object_name = 'pesobrutor49'
    form_class = PesobrutoForm
    success_url = reverse_lazy("laboratorio_control_calidad:encabezador49_create")

class pesobrutor49_update(generic.UpdateView):
    model = Pesobruto
    template_name = 'crud_VolumenNetoR49/pesoBruto_Create.html' 
    form_class = PesobrutoForm
    success_url = reverse_lazy('laboratorio_control_calidad:pesobrutor49_list')
    context_object_name = 'pesobrutor49'

class pesobrutor49_delete(generic.DeleteView):
    model = Pesobruto
    template_name = 'crud_VolumenNetoR49/pesoBruto_Delete.html'
    context_object_name = 'pesobrutor49'
    success_url = reverse_lazy('laboratorio_control_calidad:encabezador49_create')

    login_url = reverse_lazy('usuarios:login')
    

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

    def get(self, request, *args, **kwargs):
        encab_form = TerminadoEncabForm()
        terminado_formset = TerminadoFormSet(queryset=producto_terminado.objects.none())
        return render(request, 'producto_terminado.html', {
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
        

   


# END--VISTA ENCABEZADO TRES FORMULARIOS  ---------------------------------------------------|

# START--PRUEBAS VISTA PESO NETO  -----------------------------------------------------------|
class Pesonetoview(LoginRequiredMixin, TemplateView):
    template_name = 'pesoNetor49_list.html'


        

class MostrarPesosView(generic.ListView):
    model = Pesobruto
    queryset = Pesobruto.objects.all()
    template_name = 'pesonetor49_list.html'
    context_object_name = 'pesos'       
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
    

class Densidadr49UpdateView(generic.UpdateView):
    model = Densidadpt
    template_name = 'crud_VolumenNetoR49/densidad_Update.html' 
    form_class = DensidadptForm
    success_url = reverse_lazy('laboratorio_control_calidad:densidadr49_List')
    context_object_name = 'densidadr49'

class Densidadr49DeleteView(generic.DeleteView):
    model = Densidadpt
    template_name = 'crud_VolumenNetoR49/densidad_Delete.html'
    context_object_name = 'densidadr49'
    success_url = reverse_lazy('laboratorio_control_calidad:densidadr49_List')
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
    success_url = reverse_lazy('laboratorio_control_calidad:pesoBrutor49_List')
    context_object_name = 'pesoBrutor49'

class PesoBrutor49DeleteView(generic.DeleteView):
    model = Pesobruto
    template_name = 'crud_VolumenNetoR49/pesoBruto_Delete.html'
    context_object_name = 'pesoBrutor49'
    success_url = reverse_lazy('laboratorio_control_calidad:pesoBrutor49_List')
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
    success_url = reverse_lazy("laboratorio_control_calidad:encabezador49_create")

class PesoEnvVacior49UpdateView(generic.UpdateView):
    model = Pesoenvvacio
    template_name = 'crud_VolumenNetoR49/pesoEnvVacior49_Create.html' 
    form_class = PesoenvvacioForm
    success_url = reverse_lazy('laboratorio_control_calidad:pesoEnvVacior49_List')
    context_object_name = 'pesoEnvVacior49'

class PesoEnvVacior49DeleteView(generic.DeleteView):
    model = Pesoenvvacio
    template_name = 'crud_VolumenNetoR49/pesoEnvVacio_Delete.html'
    context_object_name = 'pesoEnvVacior49'
    success_url = reverse_lazy('laboratorio_control_calidad:pesoEnvVacior49_List')
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




class EncabR49CreateView(FormView):

    template_name = 'encabezador49V2_Create.html'
    form_class = EncabR49V2Form
    success_url = reverse_lazy('laboratorio_control_calidad:encabezador49_list')  # Redirige a una vista después de guardar

    def form_valid(self, form):
        # Guarda el formulario (crea una instancia del modelo y guarda en la base de datos)
        form.save()
        # Puedes realizar otras acciones aquí, como enviar notificaciones
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['datosPesoBruto'] = Pesobruto.objects.all()
        context['datosDensidad'] = Densidadpt.objects.all()
        context['datosPesoEnvVacio'] = Pesoenvvacio.objects.all()
        return context


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

class TerminadoDelete(generic.DeleteView):
    model = terminadoEncab
    template_name = 'terminadoDelete.html'
    context_object_name = 'terminado'
    success_url = reverse_lazy('laboratorio_control_calidad:TerminadoList')
    
class permisos(generic.UpdateView):
    model = terminadoEncab
    form_class = permisosForm
    template_name = "modificar.html"
    success_url = reverse_lazy('laboratorio_control_calidad:TerminadoList')
    login_url = reverse_lazy('usuarios:login')
   
