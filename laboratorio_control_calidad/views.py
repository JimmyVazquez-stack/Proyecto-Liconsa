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
from django.shortcuts import get_object_or_404, redirect #calculos para Formator49
from django.db.models import Avg, Sum, F, DecimalField #calculos para Formator49
from django.contrib import messages 
from django.db import transaction
from laboratorio_control_calidad.models import Densidadpt, Pesoenvvacio, Pesobruto, EncabTablaR49
from .forms import *


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



#START--VISTA ENCABEZADO TRES FORMULARIOS FORMATO R49 J.Carlos -----------------------------------|

class Encabezador49View(generic.ListView):
    model = EncabTablaR49
    queryset = EncabTablaR49.objects.all()
    template_name = 'encabezador49_List.html'
    context_object_name = 'EncabTablaR49'



class Encabezador49Create(View):
    success_url = reverse_lazy('laboratorio_control_calidad:encabezador49_list')

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
            with transaction.atomic():
                encab_instance = encab_form.save()
                densidad_valid = self._process_formset(Densidadpt_formset, encab_instance)
                pesoenvVacio_valid = self._process_formset(Pesoenvvacio_formset, encab_instance)
                pesoBruto_valid = self._process_formset(Pesobruto_formset, encab_instance)

                if densidad_valid and pesoenvVacio_valid and pesoBruto_valid:
                  return redirect(self.success_url)

                else:
                    messages.error(self.request, 'Algunos formsets contienen errores. Por favor, revise los campos.')
        else:
            messages.error(self.request, 'Error en el formulario principal.')
        
        return render(request, 'encabezador49_Create.html', {
            'encab_form': encab_form,
            'Densidadpt_formset': Densidadpt_formset,
            'Pesoenvvacio_formset': Pesoenvvacio_formset,
            'Pesobruto_formset': Pesobruto_formset,
        })

       

    def _process_formset(self, formset, encab_instance):
        valid = True
        for form in formset:
            if form.is_valid() and self._has_data(form.cleaned_data):
                instance = form.save(commit=False)
                instance.encabezado = encab_instance
                instance.save()
            elif not form.is_valid() and self._has_data(form.cleaned_data):
                valid = False
                messages.error(self.request, f'Error en el formset de {formset.form}: {form.errors}')
                break
        if not valid:
            messages.error(self.request, f'El formset de {formset.form} tiene registros incompletos.')
        return valid

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
    success_url = reverse_lazy('laboratorio_control_calidad:encabezador49_list')

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
    success_url = reverse_lazy('laboratorio_control_calidad:encabezador49_list')

    

class Pesonetoview(LoginRequiredMixin, TemplateView):
    template_name = 'pesoNetor49_list.html'
# END--VISTA ENCABEZADO TRES FORMULARIOS  ---------------------------------------------------|



#prueba mostrar peso neto
#def mostrar_pesos(request):
#   pesos = Pesoenvvacio.objects.all()
#  return render(request, 'pesonetor49_list.html', {'pesos': pesos})
###   
        

class MostrarPesosView(generic.ListView):
    model = Pesobruto
    queryset = Pesobruto.objects.all()
    template_name = 'pesonetor49_list.html'
    context_object_name = 'pesos'       
        
        
