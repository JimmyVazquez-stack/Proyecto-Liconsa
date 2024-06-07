from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import LecheriaForm
from .models import Lecheria,  Rotos
from django.http import JsonResponse
from django.views import View
from django.db.models import F


# Create your views here.
class LecheriaListView(TemplateView):
    template_name = 'lecherias_list.html'
    


class AñadirLecheriaView(CreateView):
    template_name = 'añadir_lecheria.html'
    form_class = LecheriaForm
    success_url = reverse_lazy('catalogos:lecherias_list')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
    
class LecheriaDataView(View):
    def get(self, request, *args, **kwargs):
        lecherias = Lecheria.objects.annotate(
            numero_ruta=F('ruta__numero'),
            nombre_poblacion=F('poblacion__nombre'),
            rotos_reportados=F('rotos__rotos_reportados')
        ).values()  # Elimina los argumentos aquí
        lecherias_list = list(lecherias)
        return JsonResponse(lecherias_list, safe=False)