#Importaciones de modelos y formularios
from .models import *
from .forms import *
#Importaciones de vistas genéricas
from django.views.generic import TemplateView, DeleteView
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
    template_name = 'complementariasR49/densidadr49_list.html'
    context_object_name = 'densidadr49'

class densidadr49_create(generic.CreateView):
    model = Densidadpt
    template_name = 'complementariasR49/densidadr49_create.html'
    context_object_name = 'densidadr49'
    form_class = DensidadptForm
    success_url = reverse_lazy("laboratorio_control_calidad:densidadr49_list")

class densidadr49_update(generic.UpdateView):
    model = Densidadpt
    template_name = 'complementariasR49/densidadr49_create.html' 
    form_class = DensidadptForm
    success_url = reverse_lazy('laboratorio_control_calidad:densidadr49_list')
    context_object_name = 'densidadr49'

class densidadr49_delete(generic.DeleteView):
    model = Densidadpt
    template_name = 'complementariasR49/densidadr49_delete.html'
    context_object_name = 'densidadr49'
    success_url = reverse_lazy('laboratorio_control_calidad:densidadr49_list')


### complementarias a formato R49 PESO ENVASE VACIO# 
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
        
        # Si hay algún error, también redirigir (esto incluye el caso donde encab_form no es válido)
        return redirect(self.success_url)
    
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
   

    
