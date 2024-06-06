from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from .models import Lecheria

class LecheriaListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'rotos.html')

class LecheriaDataView(View):
    def get(self, request, *args, **kwargs):
        lecherias_list = list(Lecheria.objects.values())
        return JsonResponse(lecherias_list, safe=False)