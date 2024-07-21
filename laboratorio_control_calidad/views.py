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
    success_url = reverse_lazy('laboratorio_control_calidad:TerminadoList')
    
class permisos(generic.UpdateView):
    model = terminadoEncab
    form_class = permisosForm
    template_name = "producto_terminado/modificar.html"
    success_url = reverse_lazy('laboratorio_control_calidad:TerminadoList')
    login_url = reverse_lazy('usuarios:login')
   

    
