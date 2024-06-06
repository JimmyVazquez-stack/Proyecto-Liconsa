from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import Lecheria
from django.db.models import F

class LecheriaListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'rotos.html')

class LecheriaDataView(View):
    def get(self, request, *args, **kwargs):
        lecherias = Lecheria.objects.annotate(
            municipio=F('poblacion__municipio'),
            numero_ruta=F('ruta__numero')
        ).values(  'numero', 'nombre', 'responsable', 'municipio', 'telefono', 'direccion','numero_ruta')
        
        lecherias_list = list(lecherias)
        return JsonResponse(lecherias_list, safe=False)