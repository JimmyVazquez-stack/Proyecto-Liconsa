<<<<<<< HEAD

from django.contrib.auth.mixins import LoginRequiredMixin 
from django.views import generic

# Create your views here.
# LoginRequiredMixin, generic.TemplateView

class Producto_no_Conforme_Home(generic.TemplateView):
    template_name = 'Prod_No_Conforme_Home.html'
    #login_url = 'login'

class Producto_no_Conforme_Registro(generic.TemplateView):
    template_name = 'Reg_Prod_No_Conforme.html'
    #login_url = 'login'
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from catalogos.models import Lecheria
from django.db.models import F
from django.views.generic import TemplateView


class LecheriaListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'rotos.html')
=======
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
>>>>>>> d2087161ed664a5d99d597d283d3efa8089d7dc6

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

<<<<<<< HEAD
class CrearMuestreoRotos(TemplateView):
    template_name = 'rotos/crear_muestreo_rotos.html'
     

class Producto_no_Conforme_Registro(generic.TemplateView):
    template_name = 'Reg_Prod_No_Conforme.html'
    #login_url = 'login'
=======
class CrearMuestreoRotos(LoginRequiredMixin,TemplateView):
    template_name = 'rotos/crear_muestreo_rotos.html'
    login_url = 'usuarios:login'
>>>>>>> d2087161ed664a5d99d597d283d3efa8089d7dc6
