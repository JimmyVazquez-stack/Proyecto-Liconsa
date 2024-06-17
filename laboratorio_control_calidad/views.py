from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.views.generic import TemplateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.views import generic 
from django.urls  import reverse_lazy
from django.views import View
from .models import *
from .forms import *
from django.contrib import messages
from django.views.generic.edit import CreateView


# Create your views here.
class index(TemplateView):
    template_name = 'index.html'

class grasas_aceites_vegetales(TemplateView):
    template_name = 'grasas_aceites_vegetales.html'

class mezcla_oleosa_vitaminas(TemplateView):
    template_name = 'mezcla_oleosa_vitaminas.html'

class pre_mezclas_vitaminas_minerales(TemplateView):
    template_name = 'pre_mezclas_vitaminas_minerales.html'

class leche_polvo_fysf(TemplateView):
    template_name = 'leche_polvo_fysf.html'

class soluciones_valoradas_ts(TemplateView):
    template_name = 'soluciones_valoradas_ts.html'

class evaluacion_sensorial(TemplateView):
    template_name = 'evaluacion_sensorial.html'

class monitoreo_medio_ambiente(TemplateView):
    template_name = 'monitoreo_medio_ambiente.html'

class limpieza_equipo_personal(TemplateView):
    template_name = 'limpieza_equipo_personal.html'

class calibracion_verificacion_equipo(TemplateView):
    template_name = 'calibracion_verificacion_equipo.html'

class verificacion_documentos(TemplateView):
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

        if encab_form.is_valid() and silos_formset.is_valid():
            encab_instance = encab_form.save()
            for form in silos_formset:
                silo = form.save(commit=False)
                silo.encabezado = encab_instance
                silo.save()
            return redirect(self.success_url)
        else:
            if not encab_form.is_valid():
                messages.error(request, f'Error en el formulario de Encab: {encab_form.errors}')
            if not silos_formset.is_valid():
                messages.error(request, f'Error en el formulario de Silos: {silos_formset.errors}')

        return render(request, 'Leche_Reconstituida_por_Silos_Encab/Leche_Reconstituida_Por_Silos_Encab_Create.html', {
            'encab_form': encab_form,
            'silos_formset': silos_formset,
        })


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
                messages.error(request, f'Error en el formulario de Encab: {encab_form.errors}')
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




#=========================[Start] Leche Reconstituida por silos [Start]==============================#



class LecheReconsSilosView(generic.ListView): 
    model =  LecheReconsSilos
    queryset = LecheReconsSilos.objects.all()
    template_name = 'Leche_Reconstituida_Por_Silos/Leche_Reconstituida_Por_Silos_List.html'
    context_object_name = 'LecheReconsSilos'

class LecheReconsSilosCreate(generic.CreateView):
    model = LecheReconsSilos
    template_name = 'Leche_Reconstituida_Por_Silos/Leche_Reconstituida_Por_Silos_Create.html'
    context_object_name = 'LecheReconsSilos'
    form_class = LecheReconsSilosForm
    success_url = reverse_lazy("Leche_Recons_Silos_List")
    
class LecheReconsSilosUpdate(generic.UpdateView):
    model = LecheReconsSilos
    template_name = 'Leche_Reconstituida_Por_Silos/Leche_Reconstituida_Por_Silos_Create.html'
    context_object_name = 'LecheReconsSilos'
    form_class = LecheReconsSilosForm
    success_url = reverse_lazy('Leche_Recons_Silos_List')

class LecheReconsSilosDelete(generic.DeleteView):
    model = LecheReconsSilos
    template_name = 'Leche_Reconstituida_Por_Silos/Leche_Reconstituida_Por_Silos_Delete.html'
    context_object_name = 'LecheReconsSilos'
    success_url = reverse_lazy('Leche_Recons_Silos_List')
    


#==========================[End] Leche Reconstituida por silos [End] ===============================#
    