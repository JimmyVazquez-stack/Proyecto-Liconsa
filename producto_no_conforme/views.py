from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from catalogos.models import Lecheria
from django.db.models import F
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class LecheriaListView(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        return render(request, 'rotos.html')
    login_url = 'usuarios:login'

class LecheriaRotosDataView(View):
    def get(self, request, *args, **kwargs):
        lecherias = Lecheria.objects.annotate(
            municipio=F('poblacion__municipio'),
            numero_ruta=F('ruta__numero'),
            nombre_poblacion=F('poblacion__nombre'),
            rotos_reportados=F('rotos__rotos_reportados')
        ).values('numero_ruta', 'numero', 'nombre', 'responsable', 'municipio', 'telefono', 'direccion', 'nombre_poblacion', 'rotos_reportados')
        
        lecherias_list = list(lecherias)
        return JsonResponse(lecherias_list, safe=False)

class CrearMuestreoRotos(LoginRequiredMixin,TemplateView):
    template_name = 'rotos/crear_muestreo_rotos.html'
    login_url = 'usuarios:login'
