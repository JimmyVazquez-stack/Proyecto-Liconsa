from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import LecheriaForm
from .models import Lecheria,  Rotos
from django.http import JsonResponse
from django.views import View
from django.db.models import F
from django.forms.models import model_to_dict
import json
from django.contrib.auth.mixins import LoginRequiredMixin



# Create your views here.
class LecheriaListView(LoginRequiredMixin,TemplateView):
    template_name = 'lecherias_list.html'
    login_url = reverse_lazy('usuarios:login')
    


class AñadirLecheriaView(LoginRequiredMixin, CreateView):
    template_name = 'añadir_lecheria.html'
    form_class = LecheriaForm
    login_url = reverse_lazy('usuarios:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    
class LecheriaDataView(LoginRequiredMixin,View):
    login_url = reverse_lazy('usuarios:login')
    def get(self, request, *args, **kwargs):
        lecherias = Lecheria.objects.annotate(
            numero_ruta=F('ruta__numero'),
            nombre_poblacion=F('poblacion__nombre'),
            rotos_reportados=F('rotos__rotos_reportados')
        ).values()  # Elimina los argumentos aquí
        lecherias_list = list(lecherias)
        return JsonResponse(lecherias_list, safe=False)
    

class ActualizarLecheriaView(View):
    login_url = reverse_lazy('usuarios:login')
    def post(self, request, *args, **kwargs):
        form_data = json.loads(request.body)
        lecheria = Lecheria.objects.get(id=form_data['id'])
        
        lecheria.numero = form_data.get('numero', lecheria.numero)
        lecheria.nombre = form_data.get('nombre', lecheria.nombre)
        lecheria.responsable = form_data.get('responsable', lecheria.responsable)
        lecheria.telefono = form_data.get('telefono', lecheria.telefono)
        lecheria.direccion = form_data.get('direccion', lecheria.direccion)
        
        ruta_id = form_data.get('ruta')
        if ruta_id is not None:
            lecheria.ruta = Ruta.objects.get(id=ruta_id)
        
        poblacion_id = form_data.get('poblacion')
        if poblacion_id is not None:
            lecheria.poblacion = Poblacion.objects.get(id=poblacion_id)
        
        lecheria.save()
        return JsonResponse(model_to_dict(lecheria), safe=False)