from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.generic import TemplateView
from django.urls import reverse_lazy 
from django.views import generic
from .models import *
from .forms import *
from usuarios.utils.mixins import GroupRequiredMixin
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views import View
from django.contrib import messages
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

"""  class TerminadoCreate(generic.CreateView):
    model = producto_terminado
    template_name = 'producto_terminado.html'
    context_object_name = 'terminado'
    form_class = TerminadoForm
    success_url = reverse_lazy("laboratorio_control_calidad:TerminadoList")

class TerminadoUpdate(generic.UpdateView):
    model = producto_terminado
    template_name = 'producto_terminado.html'
    context_object_name = 'terminado'
    form_class = TerminadoForm
    success_url = reverse_lazy('laboratorio_control_calidad:TerminadoList')



"""

class TerminadoEncabView(generic.ListView):
    model = terminadoEncab
    queryset = terminadoEncab.objects.all()
    template_name = 'pterminado_encab_list.html'
    context_object_name = 'terminadoEncab'

class TerminadoEncabCreate(View):
    success_url = reverse_lazy('laboratorio_control_calidad:TerminadoList')

    def get(self, request, *args, **kwargs):
        encab_form = TerminadoEncabForm()
        termformset = TerminadoFormSet(queryset=producto_terminado.objects.none())
        return render(request, 'producto_terminado.html', {
            'encab_form': encab_form,
            'termformset': termformset,
        })

    def post(self, request, *args, **kwargs):
        encab_form = TerminadoEncabForm(request.POST)
        termformset = TerminadoFormSet(request.POST)

        if encab_form.is_valid():
            encab_instance = encab_form.save()
            terminado_valid = True
            for form in termformset:
                if form.is_valid() and self._has_data(form.cleaned_data):
                    terminado = form.save(commit=False)
                    terminado.encabezado = encab_instance
                    terminado.save()
                elif not form.is_valid() and self._has_data(form.cleaned_data):
                    terminado_valid = False
                    break

            if terminado_valid:
                return redirect(self.success_url)
            else:
                messages.error(request, f'Error en el formulario de Silos: {termformset.errors}')
        else:
            messages.error(request, f'Error en el formulario de Encab: {encab_form.errors}')

        return render(request, 'producto_terminado.html', {
            'encab_form': encab_form,
            'termformset': termformset,
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

class TerminadoEncabUpdate(View):
    success_url = reverse_lazy('laboratorio_control_calidad:TerminadoList')

    def get(self, request, *args, **kwargs):
        encab = get_object_or_404(terminadoEncab, pk=kwargs['pk'])
        encab_form = TerminadoEncabForm(instance=encab)
        termformset = TerminadoFormSet(instance=encab)
        return render(request, 'producto_terminado.html', {
            'encab_form': encab_form,
            'termformset': termformset,
        })

    def post(self, request, *args, **kwargs):
        encab = get_object_or_404(terminadoEncab, pk=kwargs['pk'])
        encab_form = TerminadoEncabForm(request.POST, instance=encab)
        termformset = TerminadoFormSet(request.POST, instance=encab)
        if encab_form.is_valid() and termformset.is_valid():
            encab = encab_form.save()
            termformset.save()  # Guarda el formset con la instancia adecuada
            return redirect(self.success_url)
        else:
            if not encab_form.is_valid():
                messages.error(request, f'Error en el formulario de Encabezado: {encab_form.errors}')
            if not termformset.is_valid():
                messages.error(request, f'Error en el formulario de Silos: {termformset.errors}')

        return render(request, 'Leche_Reconstituida_por_Silos_Encab/Leche_Reconstituida_Por_Silos_Encab_Create.html', {
            'encab_form': encab_form,
            'termformset': termformset,
        })
    
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
   

    
