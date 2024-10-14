from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from catalogos.models import Lecheria
from .models import *
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .forms import *
from django.urls import reverse_lazy 


class LecheriaListView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        return render(request, 'rotos.html')
    login_url = 'usuarios:login'

class LecheriaRotosDataView(View):
    def get(self, request, *args, **kwargs):
        lecherias = Lecheria.objects.annotate(
            municipio=('poblacion__municipio'),
            numero_ruta=('ruta__numero'),
            nombre_poblacion=('poblacion__nombre'),
            rotos_reportados=('rotos__rotos_reportados')
        ).values('numero_ruta', 'numero', 'nombre', 'responsable', 'municipio', 'telefono', 'direccion', 'nombre_poblacion', 'rotos_reportados')
        
        lecherias_list = list(lecherias)
        return JsonResponse(lecherias_list, safe=False)

class CrearMuestreoRotos(LoginRequiredMixin,TemplateView):
    template_name = 'rotos/crear_muestreo_rotos.html'
    login_url = 'usuarios:login'

# Mal sellados ENCABEZADO--------------------------------
class malSelladosEncabView(generic.ListView):
    model = MalSelladosEncab
    queryset = MalSelladosEncab.objects.all()
    template_name = 'MalSellados/MalSEncabList.html'
    context_object_name = 'encab'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = MalSelladosEncabForm()
        return context
    
    def post(self, request, *args, **kwargs):
        form = MalSelladosEncabForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('producto_no_conforme:ms_encabView')
        else:
            print("Form errors:", form.errors)  # Agrega esta línea para ver los errores del formulario
        return self.get(request, *args, **kwargs)
    
class malSelladosUpdate(generic.UpdateView):
    model = MalSelladosEncab
    template_name = 'MalSellados/malSelladosCreate.html'
    context_object_name = 'Encab'
    form_class = MalSelladosEncabForm
    success_url = reverse_lazy('producto_no_conforme:ms_encabUpdate')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        encab_object = self.get_object()
        context['term'] = MalSellados.objects.filter(encabezado=encab_object)

        # Si se recibe un ID en el GET, se está editando un registro; de lo contrario, es un nuevo registro.
        term_id = self.request.GET.get('term_id')
        if term_id:
            try:
                term_instance = MalSellados.objects.get(id=term_id)
                nuevo_form = MalSelladosForm(instance=term_instance)
                context['edit_mode'] = True
            except MalSellados.DoesNotExist:
                nuevo_form = MalSelladosForm(initial={'encabezado': encab_object})
                context['edit_mode'] = False
        else:
            nuevo_form = MalSelladosForm(initial={'encabezado': encab_object})
            context['edit_mode'] = False

        # Filtrar las lecherías por la ruta seleccionada
        if 'ruta' in self.request.GET:
            ruta_id = self.request.GET['ruta']
            lecherias = Lecheria.objects.filter(ruta_id=ruta_id)
        else:
            lecherias = Lecheria.objects.none()  # No mostrar lecherías si no hay ruta seleccionada

        context['lecherias'] = lecherias
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
                term_instance = MalSellados.objects.get(id=term_id)
                nuevo_form = MalSelladosForm(request.POST, instance=term_instance)
            except MalSellados.DoesNotExist:
                nuevo_form = MalSelladosForm(request.POST)
        else:
            nuevo_form = MalSelladosForm(request.POST)

        # Guardar el formulario de encabezado si se presionó su botón de guardar
        if 'submit-encab-form' in request.POST:
            if form.is_valid():
                form.save()
            return redirect(self.success_url)
        else:
            print(form.errors)  # Mostrar errores del formulario en la consola para depurar

            # Guardar el formulario de nuevo producto_terminado si se presionó su botón de guardar
        if 'submit-nuevo-form' in request.POST and nuevo_form.is_valid():
            nuevo_form.save()
            return redirect(request.path)

        # En caso de errores, renderizar los formularios con los datos ya ingresados
        context = self.get_context_data()
        context['form'] = form
        context['nuevo_form'] = nuevo_form
        return self.render_to_response(context)


    
class MalSelladosDelete(generic.DeleteView):
    model = MalSelladosEncab
    template_name = 'MalSellados/MalSelladosDelete.html'
    context_object_name = 'term'
    success_url = reverse_lazy('producto_no_conforme:ms_encabView')
