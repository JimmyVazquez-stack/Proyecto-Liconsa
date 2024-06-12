from django.shortcuts import render
from django.views.generic import TemplateView
from laboratorio_control_calidad.forms import TablaR49Form
from laboratorio_control_calidad.models import TablaR49
from .forms import TablaR49Form
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
    

class tabla_r49(TemplateView): 
    template_name = 'tabla_r49.html' 


class crear_registror49(CreateView):
    template_name = 'crear_registror49.html'
    form_class = TablaR49
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


    # 
    # get(self, request, *args, **kwargs): 

    #     form = TablaR49Form(request.POST) 
    #     if form.is_valid():
    #         num_maquina = formulario.cleaned_data['num_maquina']
    #         num_datos = formulario.cleaned_data['num_datos']
    #         promedio = formulario.cleaned_data['promedio']
    #         desv_std = formulario.cleaned_data['desv_std']
    #         maximo = formulario.cleaned_data['maximo']
    #         minimo = formulario.cleaned_data['minimo']
    #         form.save() 
    #     return render(request, 'tabla_r49.html', {'form': form})
    
        #return self.render_to_response({'form': form}) 
    


     