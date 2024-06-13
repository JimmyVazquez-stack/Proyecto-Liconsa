from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from catalogos.models import Lecheria
from django.db.models import F
from django.views.generic import TemplateView
#para generar pdfs 
from django.http import FileResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.http import HttpResponse

def render_pdf_view(request):
    template_path = 'rotos/ver_reporte.html'
    context = {}  # Añade aquí las variables de contexto que necesites
    # Renderiza la plantilla con el contexto
    response = get_template(template_path).render(context)
    # Crea un archivo PDF en memoria
    pdf = BytesIO()
    pisa_status = pisa.CreatePDF(response, dest=pdf)
    # Si ocurrió un error, devuelve un mensaje
    if pisa_status.err:
        return HttpResponse('Ocurrió un error al generar el PDF: ' + str(pisa_status.err))
    # Si todo está bien, devuelve el PDF
    pdf.seek(0)
    return FileResponse(pdf, content_type='application/pdf')


class LecheriaListView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'rotos.html')

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

class CrearMuestreoRotos(TemplateView):
    template_name = 'rotos/crear_muestreo_rotos.html'
     
class VerReporteView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'rotos/ver_reporte.html')      