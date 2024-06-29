from django.shortcuts import render
from django.views.generic import TemplateView
from laboratorio_control_calidad.forms import *
from .models import *
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic, View

from usuarios.utils.mixins import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from usuarios.models import Usuario
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission #Importamos el modelo Permission

# Create your views here.
class index(LoginRequiredMixin,TemplateView, PermissionRequiredMixin ):
    model = get_user_model()
    template_name = 'index.html'
    login_url = reverse_lazy('usuarios:login')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_usuarios'] = self.model.objects.count()
        
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

    login_url = reverse_lazy('usuarios:login')
    
#VISTA ENCABEZADO TRES FORMULARIOS START

class Encabezador49View(generic.ListView):
    model = EncabTablaR49
    queryset = EncabTablaR49.objects.all()
    template_name = 'encabezador49_List.html'
    context_object_name = 'EncabTablaR49'

class Encabezador49Create(View):
    success_url = reverse_lazy('laboratorio_control_calidad:encabezador49_List')

    def get(self, request, *args, **kwargs):
        encab_form = EncabTablaR49Form()
        Densidadpt_formset = DensidadptFormSet(queryset=Densidadpt.objects.none())
        Pesoenvvacio_formset = PesoenvvacioFormSet(queryset=Pesoenvvacio.objects.none())
        Pesobruto_formset = PesobrutoFormSet(queryset=Pesobruto.objects.none())
        return render(request, 'encabezador49_Create.html', {
            'encab_form': encab_form,
            'Densidadpt_formset': Densidadpt_formset,
            'Pesoenvvacio_formset': Pesoenvvacio_formset,
            'Pesobruto_formset': Pesobruto_formset,
        })

    def post(self, request, *args, **kwargs):
        encab_form = EncabTablaR49Form(request.POST)
        Densidadpt_formset = DensidadptFormSet(request.POST)
        Pesoenvvacio_formset = PesoenvvacioFormSet(request.POST)
        Pesobruto_formset = PesobrutoFormSet(request.POST)

        if encab_form.is_valid():
            encab_instance = encab_form.save()

              #PARA FORMSET1
            silos_valid = True
            for form in Densidadpt_formset:
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
                messages.error(request, f'Error en el formulario de Densidad: {Densidadpt_formset.errors}')
            #END FORMSET1

            #PARA FORMSET2
            silos_valid = True
            for form in Pesoenvvacio_formset:
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
                messages.error(request, f'Error en el formulario de Peso envase vacio: {Pesoenvvacio_formset.errors}')  
            #END FORMSET2

            #PARA FORMSET3
            silos_valid = True
            for form in Pesobruto_formset:
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
                messages.error(request, f'Error en el formulario de Silos: {Pesobruto_formset.errors}')
              #END FORMSET3


        else:
            messages.error(request, f'Error en el formulario de Encab: {encab_form.errors}')

        return render(request, 'encabezador49_Create.html', {
            'encab_form': encab_form,
            'Densidadpt_formset': Densidadpt_formset,
            'Pesoenvvacio_formset': Pesoenvvacio_formset,
            'Pesobruto_formset': Pesobruto_formset,


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
    

class Encabezador49Update(View):
    success_url = reverse_lazy('laboratorio_control_calidad:encabezador49_List')

    def get(self, request, *args, **kwargs):
        encab = get_object_or_404(EncabTablaR49, pk=kwargs['pk'])
        encab_form = EncabTablaR49Form(instance=encab)
        Densidadpt_formset = DensidadptFormSet(instance=encab)
        Pesoenvvacio_formset = PesoenvvacioFormSet(instance=encab)
        Pesobruto_formset = PesobrutoFormSet(instance=encab)
        return render(request, 'encabezador49_Create.html', {
            'encab_form': encab_form,
            'Densidadpt_formset': Densidadpt_formset,
            'Pesoenvvacio_formset': Pesoenvvacio_formset,
            'Pesobruto_formset': Pesobruto_formset,
        })

    def post(self, request, *args, **kwargs):
        encab = get_object_or_404(EncabTablaR49, pk=kwargs['pk'])
        encab_form = EncabTablaR49Form(request.POST, instance=encab)
        Densidadpt_formset = DensidadptFormSet(request.POST, instance=encab)
        Pesoenvvacio_formset = PesoenvvacioFormSet(request.POST, instance=encab)
        Pesobruto_formset = PesobrutoFormSet(request.POST, instance=encab)
        
        #PARA FORMSET1
        if encab_form.is_valid() and Densidadpt_formset.is_valid():
            encab = encab_form.save()
            Densidadpt_formset.save()  # Guarda el formset con la instancia adecuada
        
            
            return redirect(self.success_url)
        else:
            if not encab_form.is_valid():
                messages.error(request, f'Error en el formulario de Encabezado: {encab_form.errors}')
            if not Densidadpt_formset.is_valid():
                messages.error(request, f'Error en el formulario de Densidad: {Densidadpt_formset.errors}')
        #END FORMSET1
    
        #PARA FORMSET2
        if encab_form.is_valid() and Pesoenvvacio_formset.is_valid():
            encab = encab_form.save()
            Pesoenvvacio_formset.save()  # Guarda el formset con la instancia adecuada
        
            
            return redirect(self.success_url)
        else:
            if not encab_form.is_valid():
                messages.error(request, f'Error en el formulario de Encabezado: {encab_form.errors}')
            if not Pesoenvvacio_formset.is_valid():
                messages.error(request, f'Error en el formulario de Peso vacio: {Pesoenvvacio_formset.errors}')
        #END FORMSET2

        #PARA FORMSET3
        if encab_form.is_valid() and Pesobruto_formset.is_valid():
            encab = encab_form.save()
            Pesobruto_formset.save()  # Guarda el formset con la instancia adecuada
        
            
            return redirect(self.success_url)
        else:
            if not encab_form.is_valid():
                messages.error(request, f'Error en el formulario de Encabezado: {encab_form.errors}')
            if not Pesobruto_formset.is_valid():
                messages.error(request, f'Error en el formulario de Peso bruto: {Pesobruto_formset.errors}')
        #END FORMSET3

        return render(request, 'encabezador49_Create.html', {
            'encab_form': encab_form,
            'Densidadpt_formset': Densidadpt_formset,
            'Pesoenvvacio_formset': Pesoenvvacio_formset,
            'Pesobruto_formset': Pesobruto_formset,
        })

   
class Encabezador49Delete(DeleteView):
    model = EncabTablaR49
    template_name = 'encabezador49_Delete.html'
    context_object_name = 'EncabTablaR49'
    success_url = reverse_lazy('encabezador49_List')
    
# VISTA ENCABEZADO TRES FORMULARIOS END 