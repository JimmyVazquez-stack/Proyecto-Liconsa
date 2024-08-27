from django.http import HttpResponse, JsonResponse
from django.views.generic import View, TemplateView
from django.db.models import Min, Max, Count, Sum, F, FloatField, DecimalField, StdDev
from django.shortcuts import render
from django.views import View
from laboratorio_control_calidad.models import *
from catalogos.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from laboratorio_control_calidad.models import LecheReconsSilos, Pesoenvvacio, Pesobruto, Densidadpt
from django.conf import settings
import requests
import statistics
from django.urls import reverse_lazy
from django.http import HttpResponse


#Importaciones de REPORTLAB
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.units import inch
#APIS REST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from laboratorio_control_calidad.models import LecheReconsSilos, producto_terminado
from .serializers import *
from django.core.exceptions import ValidationError
from django.utils.dateparse import parse_date
from django.db.models import Avg, Min, Max, Sum


# Vista para el reporte mensual para el laboratorio de control de calidad
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from django.conf import settings
import requests

#Vista para el reporte mensual para el laboratorio de control de calidad
class ReporteMensualView(LoginRequiredMixin, TemplateView):
        def get(self, request, *args, **kwargs):
            producto_id = request.GET.get('producto_id')
            fecha_inicio = request.GET.get('fecha_inicio')
            fecha_fin = request.GET.get('fecha_fin')
            datos = []

            if fecha_inicio and fecha_fin and producto_id:
                api_url = f"{settings.API_BASE_URL}api/composicion_fisicoquimica/?fecha_fin={fecha_fin}&fecha_inicio={fecha_inicio}&producto_id={producto_id}"
                
                try:
                    response = requests.get(api_url)
                    response.raise_for_status()
                    datos = response.json()
                except requests.exceptions.RequestException as e:
                    return HttpResponse(f"Error al obtener datos: {str(e)}", status=500)
            
            context = {
                'datos': datos,
                'fecha_inicio': fecha_inicio,
                'fecha_fin': fecha_fin,
                'producto_id': producto_id
            }
            print(context)
            return render(request, 'mensual_reporte.html', context)



class ComposicionFisicoquimicaDataView(APIView):
    def get(self, request, *args, **kwargs):
        tipo_producto = request.query_params.get('tipo_producto')
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')

        if not fecha_inicio or not fecha_fin:
            return Response({"error": "Se requieren ambos parámetros 'fecha_inicio' y 'fecha_fin' en el formato 'YYYY-MM-DD'"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            fecha_inicio = parse_date(fecha_inicio)
            fecha_fin = parse_date(fecha_fin)
            
            if fecha_inicio is None or fecha_fin is None:
                raise ValidationError("Formato de fecha incorrecto. Use 'YYYY-MM-DD'.")
            
            # Filtrar por tipo_producto y rango de fechas
            if tipo_producto:
                datos_leche_reconsilos = LecheReconsSilos.objects.filter(
                    producto__tipo_producto__nombre=tipo_producto,
                    fecha_Hora__date__range=[fecha_inicio, fecha_fin]
                ).select_related('encabezado')

                datos_producto_terminado = producto_terminado.objects.filter(
                    producto__tipo_producto__nombre=tipo_producto,
                    encabezado__fecha__range=[fecha_inicio, fecha_fin]
                )
            else:
                datos_leche_reconsilos = LecheReconsSilos.objects.filter(
                    fecha_Hora__date__range=[fecha_inicio, fecha_fin]
                ).select_related('encabezado')

                datos_producto_terminado = producto_terminado.objects.filter(
                    encabezado__fecha__range=[fecha_inicio, fecha_fin]
                )
            
        except ValidationError:
            return Response({"error": "Formato de fecha incorrecto. Use 'YYYY-MM-DD'"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Error en el rango de fechas."}, status=status.HTTP_400_BAD_REQUEST)

        # Agrupar por producto_id y calcular promedios, valores mínimos y máximos
        estadisticas_leche_recon_silos = datos_leche_reconsilos.values('producto__nombre').annotate(
            producto_id = F('producto_id'),

            numero_muestras=Count('id'),

            promedio_temperatura=Avg('temperatura'),
            minimo_temperatura=Min('temperatura'),
            maximo_temperatura=Max('temperatura'),

            promedio_densidad=Avg('densidad'),
            minimo_densidad=Min('densidad'),
            maximo_densidad=Max('densidad'),

            promedio_s_g_w_v=Avg('s_g_w_v'),
            minimo_s_g_w_v=Min('s_g_w_v'),
            maximo_s_g_w_v=Max('s_g_w_v'),

            promedio_s_n_g_Stsg_wv=Avg('s_n_g_Stsg_wv'),
            minimo_s_n_g_Stsg_wv=Min('s_n_g_Stsg_wv'),
            maximo_s_n_g_Stsg_wv=Max('s_n_g_Stsg_wv'),

            promedio_st_wv=Avg('st_wv'),
            minimo_st_wv=Min('st_wv'),
            maximo_st_wv=Max('st_wv'),

        ).order_by('producto_id')

        estadisticas_producto_terminado = datos_producto_terminado.values('producto__nombre').annotate(
            producto_id = F('producto_id'),

            numero_muestras=Count('id'),

            promedio_temperatura=Avg('temperatura'),
            minimo_temperatura=Min('temperatura'),
            maximo_temperatura=Max('temperatura'),

            promedio_densidad=Avg('densidad'),
            minimo_densidad=Min('densidad'),
            maximo_densidad=Max('densidad'),

            promedio_s_g_w_v=Avg('sg'),
            minimo_s_g_w_v=Min('sg'),
            maximo_s_g_w_v=Max('sg'),

            promedio_s_n_g_Stsg_wv=Avg('sng'),
            minimo_s_n_g_Stsg_wv=Min('sng'),
            maximo_s_n_g_Stsg_wv=Max('sng'),

            promedio_st_wv=Avg('st'),
            minimo_st_wv=Min('st'),
            maximo_st_wv=Max('st'),

        ).order_by('producto_id')

        estadisticas_ph_leche_recon_silos= datos_leche_reconsilos.values('producto__nombre').annotate(
            numero_muestras=Count('id'),

            promedio_ph=Avg('ph'),
            minimo_ph=Min('ph'),
            maximo_ph=Max('ph'),
               
        ).order_by('producto_id')

        estadisticas_produccion_producto_terminado = datos_producto_terminado.values('producto__nombre').annotate(
            produccion_ventas=Sum('volumen'),
        ).order_by('producto_id')

        estadisticas_produccion_leche_recon_silos = datos_leche_reconsilos.values('producto__nombre').annotate(
            produccion_real=Sum('volumen'),
        ).order_by('producto_id')
        
        observaciones_leche_recon_silos = datos_leche_reconsilos.values(
            'encabezado__folio',
            'encabezado__observaciones',
            'producto_id'
        ).order_by('producto_id')

        observaciones_unicas = []
        observacion_anterior = None

        for observacion in observaciones_leche_recon_silos:
            if observacion['encabezado__observaciones'] != observacion_anterior:
                observaciones_unicas.append(observacion)
                observacion_anterior = observacion['encabezado__observaciones']
        
        response_data = {
            'estadisticas_leche_recon': estadisticas_leche_recon_silos, 
            'estadisticas_producto_terminado': estadisticas_producto_terminado,
            'estadisticas_ph_leche_recon_silos': estadisticas_ph_leche_recon_silos,
            'estadisticas_produccion_producto_terminado': estadisticas_produccion_producto_terminado,
            'estadisticas_produccion_leche_recon_silos': estadisticas_produccion_leche_recon_silos,
            'observaciones_leche_recon_silos': observaciones_unicas,
        }
        
        return Response(response_data, status=status.HTTP_200_OK)


class TipoPorductoDataView(APIView):
    def get(self, request, *args, **kwargs):
        tipos_productos = TipoProducto.objects.all()
        serializer = TipoProductoSerializer(tipos_productos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class PDFGeneratorCalidadMicrobiologicaView(View):
    pass

class PDFGeneratorPesoEnvaseVacioView(View):
    pass

class PDFGeneratorPesoNetoView(View):
    pass

class PDFGeneratorView(View):
    def get(self, request, *args, **kwargs):
        # Obtener las fechas desde los parámetros de la solicitud
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        producto_id = request.GET.get('producto_id')
        
        # Imprimir para depuración
        print("Fecha Inicio:", fecha_inicio)
        print("Fecha Fin:", fecha_fin)
        # Crear la respuesta del HttpResponse con el tipo de contenido correcto
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'

        # Crear el objeto PDF con márgenes personalizados
        doc = SimpleDocTemplate(
            response,
            pagesize=landscape(letter),
            topMargin=0.5 * inch,    # Ajusta el margen superior según sea necesario
            bottomMargin=0.5 * inch, # Ajusta el margen inferior según sea necesario
            leftMargin=0.5 * inch,   # Ajusta el margen izquierdo según sea necesario
            rightMargin=0.5 * inch   # Ajusta el margen derecho según sea necesario
        )

        imagen = Image("static/img/Liconsa.png", width=100, height=15)

         # Función para manejar valores None
        def safe_value(value, default="N/A"):
            return default if value is None else value

         # Consulta a la API para obtener los datos
        datos = {}
        if fecha_inicio and fecha_fin and producto_id:
            api_url = f"{settings.API_BASE_URL}api/composicion_fisicoquimica/?fecha_inicio={fecha_inicio}&fecha_fin={fecha_fin}&producto_id={producto_id}"
            
            try:
                api_response = requests.get(api_url)
                api_response.raise_for_status()
                datos = api_response.json()
            except requests.exceptions.RequestException as e:
                return HttpResponse(f"Error al obtener datos: {str(e)}", status=500)
        # Fin de la consulta a la API

        # Extraer datos de las estadísticas
        estadisticas_leche_recon = datos.get('estadisticas_leche_recon', [])
        estadisticas_producto_terminado = datos.get('estadisticas_producto_terminado', [])
        estadisticas_ph_leche_recon_silos = datos.get('estadisticas_ph_leche_recon_silos', [])
        datos_observaciones = datos.get('observaciones_leche_recon_silos', [])
        datos_produccion_real = datos.get('estadisticas_produccion_leche_recon_silos', [])
        datos_produccion_ventas = datos.get('estadisticas_produccion_producto_terminado', [])
        datos_encabezado = datos.get('datos_encabezado', [])
        

        #Tabla de encabezado - Inicio
        datos_encabezado_table1 = [
            ['LICONSA PLANTA TLAXCALA S.A DE C.V', '', ''],
            ['PERIODO REPORTADO:','HOY', 'HOY'],
        ]

        #Datos de encabezado tabla 1

        tabla_encabezado1 = Table(datos_encabezado_table1)
        tabla_encabezado1.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.white),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('SPAN', (0, 0), (2, 0)),  # Fusionar la primera fila
        ]))


        datos_encabezado_table2 = [
            ['PRODUCTO:', 'LPD'],
            ['FECHA DE EMISION:', 'HOY'],
        ]

        #Datos de encabezado tabla 2

        tabla_encabezado2 = Table(datos_encabezado_table2)
        tabla_encabezado2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.white),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.white),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ]))

        tabla_contenedora_encabezado = Table([
            [tabla_encabezado1, tabla_encabezado2, imagen]
        ])
        tabla_contenedora_encabezado.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
            ('ALIGN', (2, 0), (2, 0), 'RIGHT'),
            ('VALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('LEFTPADDING', (0, 0), (-1, -1), 0),# Eliminar padding a la izquierda para alinear al máximo
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),# Eliminar padding a la derecha
            ('TOPPADDING', (0, 0), (-1, -1), 0), # Eliminar padding en la parte superior
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0)# Eliminar padding en la parte inferior
        ]))

        #Tabla de encabezado - Fin

        #Tabla de composición fisicoquímica - Inicio
        composicion_fisicoquimica_data = [
            ['Composicion Fisioquimica', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            ["Puntos de Evaluación", "N", "Densidad", "", "", "", "Grasa", "", "", "", "SNG", "", "", "", "Proteínas", "", "", "", "Temperatura", "", "", ""],
            ["", "", "g/mL", "", "", "", "g/L", "", "", "", "g/L", "", "", "", "g/L", "", "", "", "C°", "", "", ""],
            ["", "", "X", "%FLE", "vMAX", "vMIN", "X", "%FLE", "vMAX", "vMIN", "X", "%FLE", "vMAX", "vMIN", "X", "%FLE", "vMAX", "vMIN", "X", "%FLE", "vMAX", "vMIN"]
        ]

         # Procesar estadísticas de leche reconstituida en silos
        for estadistica in estadisticas_producto_terminado:
            punto_evaluacion_producto_terminado = safe_value(estadistica.get('producto__nombre'))
            numero_muestras_producto_terminado = safe_value(estadistica.get('numero_muestras'))
            promedio_temperatura_producto_terminado = safe_value(estadistica.get('promedio_temperatura'))
            minimo_temperatura_producto_terminado = safe_value(estadistica.get('minimo_temperatura'))
            maximo_temperatura_producto_terminado = safe_value(estadistica.get('maximo_temperatura'))
            promedio_densidad_producto_terminado = safe_value(estadistica.get('promedio_densidad'))
            minimo_densidad_producto_terminado = safe_value(estadistica.get('minimo_densidad'))
            maximo_densidad_producto_terminado = safe_value(estadistica.get('maximo_densidad'))
            promedio_grasa_producto_terminado = safe_value(estadistica.get('promedio_s_g_w_v'))
            minimo_grasa_producto_terminado = safe_value(estadistica.get('minimo_s_g_w_v'))
            maximo_grasa_producto_terminado = safe_value(estadistica.get('maximo_s_g_w_v'))
            promedio_sng_producto_terminado = safe_value(estadistica.get('promedio_s_n_g_Stsg_wv'))
            minimo_sng_producto_terminado = safe_value(estadistica.get('minimo_s_n_g_Stsg_wv'))
            maximo_sng_producto_terminado = safe_value(estadistica.get('maximo_s_n_g_Stsg_wv'))
            promedio_sngt_producto_terminado = safe_value(estadistica.get('promedio_st_wv'))
            minimo_sngt_producto_terminado = safe_value(estadistica.get('minimo_st_wv'))
            maximo_sngt_producto_terminado = safe_value(estadistica.get('maximo_st_wv'))
            
            # Agregar fila con los datos procesados
            composicion_fisicoquimica_data.append([
                punto_evaluacion_producto_terminado,
                numero_muestras_producto_terminado,
                f'{promedio_densidad_producto_terminado:.1f}',  # Limitar a 1 decimal
                "fle",
                f'{maximo_densidad_producto_terminado:.1f}',    # Limitar a 1 decimal
                f'{minimo_densidad_producto_terminado:.1f}',    # Limitar a 1 decimal
                f'{promedio_grasa_producto_terminado:.1f}',     # Limitar a 1 decimal
                "fle",
                f'{maximo_grasa_producto_terminado:.1f}',       # Limitar a 1 decimal
                f'{minimo_grasa_producto_terminado:.1f}',       # Limitar a 1 decimal
                f'{promedio_sng_producto_terminado:.1f}',       # Limitar a 1 decimal
                "fle",
                f'{maximo_sng_producto_terminado:.1f}',         # Limitar a 1 decimal
                f'{minimo_sng_producto_terminado:.1f}',         # Limitar a 1 decimal
                f'{promedio_sngt_producto_terminado:.1f}',      # Limitar a 1 decimal
                "fle",
                f'{maximo_sngt_producto_terminado:.1f}',        # Limitar a 1 decimal
                f'{minimo_sngt_producto_terminado:.1f}',        # Limitar a 1 decimal
                f'{promedio_temperatura_producto_terminado:.1f}', # Limitar a 1 decimal
                "fle",
                f'{maximo_temperatura_producto_terminado:.1f}',  # Limitar a 1 decimal
                f'{minimo_temperatura_producto_terminado:.1f}'   # Limitar a 1 decimal
            ])

        # Procesar estadísticas de leche reconstituida en silos
        for estadistica in estadisticas_leche_recon:
            punto_evaluacion_leche_recon = Paragraph(safe_value(estadistica.get('producto__nombre')),style=ParagraphStyle(name='Normal', fontSize=8.5))
            numero_muestras_leche_recon = safe_value(estadistica.get('numero_muestras'))
            promedio_temperatura_leche_recon = safe_value(estadistica.get('promedio_temperatura'))
            minimo_temperatura_leche_recon = safe_value(estadistica.get('minimo_temperatura'))
            maximo_temperatura_leche_recon = safe_value(estadistica.get('maximo_temperatura'))
            promedio_densidad_leche_recon = safe_value(estadistica.get('promedio_densidad'))
            minimo_densidad_leche_recon = safe_value(estadistica.get('minimo_densidad'))
            maximo_densidad_leche_recon = safe_value(estadistica.get('maximo_densidad'))
            promedio_grasa_leche_recon = safe_value(estadistica.get('promedio_s_g_w_v'))
            minimo_grasa_leche_recon = safe_value(estadistica.get('minimo_s_g_w_v'))
            maximo_grasa_leche_recon = safe_value(estadistica.get('maximo_s_g_w_v'))
            promedio_sng_leche_recon = safe_value(estadistica.get('promedio_s_n_g_Stsg_wv'))
            minimo_sng_leche_recon = safe_value(estadistica.get('minimo_s_n_g_Stsg_wv'))
            maximo_sng_leche_recon = safe_value(estadistica.get('maximo_s_n_g_Stsg_wv'))
            promedio_sngt_leche_recon = safe_value(estadistica.get('promedio_st_wv'))
            minimo_sngt_leche_recon = safe_value(estadistica.get('minimo_st_wv'))
            maximo_sngt_leche_recon = safe_value(estadistica.get('maximo_st_wv'))
            
            # Agregar fila con los datos procesados
            composicion_fisicoquimica_data.append([
                punto_evaluacion_leche_recon,
                numero_muestras_leche_recon,
                f'{promedio_densidad_leche_recon:.1f}',  # Limitar a 1 decimal
                "fle",
                f'{maximo_densidad_leche_recon:.1f}',    # Limitar a 1 decimal
                f'{minimo_densidad_leche_recon:.1f}',    # Limitar a 1 decimal
                f'{promedio_grasa_leche_recon:.1f}',     # Limitar a 1 decimal
                "fle",
                f'{maximo_grasa_leche_recon:.1f}',       # Limitar a 1 decimal
                f'{minimo_grasa_leche_recon:.1f}',       # Limitar a 1 decimal
                f'{promedio_sng_leche_recon:.1f}',       # Limitar a 1 decimal
                "fle",
                f'{maximo_sng_leche_recon:.1f}',         # Limitar a 1 decimal
                f'{minimo_sng_leche_recon:.1f}',         # Limitar a 1 decimal
                f'{promedio_sngt_leche_recon:.1f}',      # Limitar a 1 decimal
                "fle",
                f'{maximo_sngt_leche_recon:.1f}',        # Limitar a 1 decimal
                f'{minimo_sngt_leche_recon:.1f}',        # Limitar a 1 decimal
                f'{promedio_temperatura_leche_recon:.1f}', # Limitar a 1 decimal
                "fle",
                f'{maximo_temperatura_leche_recon:.1f}',  # Limitar a 1 decimal
                f'{minimo_temperatura_leche_recon:.1f}'   # Limitar a 1 decimal
            ])

        tabla_fisicoquimica = Table(composicion_fisicoquimica_data)
        tabla_fisicoquimica.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ('SPAN', (0, 0), (-1, 0)),  # Fusionar toda la primera fila
            ('SPAN', (2, 1), (5, 1)),  # Densidad
            ('SPAN', (6, 1), (9, 1)),  # Grasa
            ('SPAN', (10, 1), (13, 1)),  # SNG
            ('SPAN', (14, 1), (17, 1)),  # Proteínas
            ('SPAN', (18, 1), (21, 1)),  # Temperatura
            ('SPAN', (2, 2), (5, 2)),  # g/ml
            ('SPAN', (6, 2), (9, 2)),  # g/ml
            ('SPAN', (10, 2), (13, 2)),  # g/ml
            ('SPAN', (14, 2), (17, 2)),  # g/ml
            ('SPAN', (18, 2), (21, 2)),  # centigrados
            ('SPAN', (0, 1), (0, 3)),  # Punto de evaluación
            ('SPAN', (1, 1), (1, 3)),  # Numero de muestras
            ('WORDWRAP', (0, 0), (-1, -1)),  # Habilitar ajuste de línea
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinear verticalmente en el medio
            ('LEFTPADDING', (0, 0), (-1, -1), 5),  # Padding izquierdo
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),  # Padding derecho
            
        ]))

        # Asignar los anchos de las columnas y las alturas de las filas
        tabla_fisicoquimica._argW = [100, 20] + [30]*20



        #Tabla de composición fisicoquímica - Fin

        #Tabla de producción - Inicio
        datos_produccion = [
            ['Datos de producción', ''],
            ['Producción real', 'Producción ventas'],
        ]

        for datos_real, datos_ventas in zip(datos_produccion_real, datos_produccion_ventas):
            produccion_real = safe_value(datos_real.get('produccion_real'))
            produccion_ventas = safe_value(datos_ventas.get('produccion_ventas'))

            datos_produccion.append([
                produccion_real,
                produccion_ventas,
            ])

        tabla_produccion = Table(datos_produccion)
        tabla_produccion.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('SPAN', (0, 0), (1, 0)),  # Fusionar la primera fila
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
        ]))

        tabla_produccion._argW = [100, 100]

        #Tabla de producción - Fin

        #Tabla de econtenido neto - Inicio
        datos_envasado = [
            ['Contenido neto', '', '', '', '', ''],
            ['N', 'mL', '', '', '', ''],
            ['', 'X', 'FLE', 'CND-2T', 'V.MAX', 'V.MIN'],
            [safe_value(100), safe_value(200), safe_value(1.5), safe_value(190), safe_value(210), safe_value(180)],
        ]

        tabla_envasado = Table(datos_envasado)
        tabla_envasado.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ('SPAN', (0, 0), (5, 0)),  # Fusionar la primera fila  
            ('SPAN', (0, 1), (0, 2)),  # Fusionar la primera columna
            ('SPAN', (1, 1), (5, 1)),  # Fusionar la segunda columna
        ]))

        tabla_envasado._argW = [40, 40, 40, 40, 40, 40]    

        #Tabla de contenido neto - Fin

        #Tabla peso envase vacio - Inicio
        datos_peso_envase_vacio = [
            ['Peso envase vacio', '', '', ''],
            ['Numero de muestras', 'X', 'V.MAX', 'V.MIN'],
        ]

        #Datos de peso envase vacio


        tabla_peso_envase_vacio = Table(datos_peso_envase_vacio)
        tabla_peso_envase_vacio.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ('SPAN', (0, 0), (3, 0)),  # Fusionar la primera fila
        ]))

        tabla_peso_envase_vacio._argW = [90, 30, 40, 40]

        #Tabla peso envase vacio - Fin

        #Tabla microbiológicos - Inicio
        datos_microbiologicos = [
            ['Calidad microbiológica', '', '', '', '', '', '', ''],
            ['Puntos de evaluación', 'N', 'Organismos coliformes', '', '', 'Aerobias', '', ''],
            ['', '', 'UFC/mL', '', '', 'UFC/mL', '', ''],
            ['', '', 'X', 'FLE', 'V.MAX', 'X', 'FLE', 'V.MAX'],
        ]

        tabla_microbiologicos = Table(datos_microbiologicos)
        tabla_microbiologicos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ('SPAN', (0, 0), (7, 0)), #Calidad microbiológica
            ('SPAN', (2, 1), (4, 1)), #Organismos coliformes
            ('SPAN', (5, 1), (7, 1)), #Aerobias
            ('SPAN', (0, 1), (0, 3)), #Puntos de evaluación 
            ('SPAN', (1, 1), (1, 3)), #N
            ('SPAN', (2, 2), (4, 2)), #ufc/ml
            ('SPAN', (5, 2), (7, 2)), #ufc/ml
        ]))


        #Tabla microbiológicos - Fin

        # Tabla de pH - Inicio
        datos_ph = [
            ['Analisis complementarios', '', '', '', '', '', '', ''],
            ['Puntos de Evaluación', 'PH', '', '', '', 'Neutralizantes', '', ''],
            ['', 'N', 'X', 'V.MAX', 'V.MIN', 'N', 'Positivo', 'Negativo'],
        ]

        for estadisticas in estadisticas_ph_leche_recon_silos:
            punto_evaluacion = Paragraph(safe_value(estadisticas.get('producto__nombre')),style=ParagraphStyle(name='Normal', fontSize=8.5))
            numero_muestras = safe_value(estadisticas.get('numero_muestras'))
            promedio_ph = safe_value(estadisticas.get('promedio_ph'))
            minimo_ph = safe_value(estadisticas.get('minimo_ph'))
            maximo_ph = safe_value(estadisticas.get('maximo_ph'))

            datos_ph.append([
                punto_evaluacion,
                numero_muestras,
                f'{promedio_ph:.1f}',  # Limitar a 1 decimal
                f'{maximo_ph:.1f}',    # Limitar a 1 decimal
                f'{minimo_ph:.1f}',    # Limitar a 1 decimal
            ])

        tabla_ph = Table(datos_ph)
        tabla_ph.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ('SPAN', (0, 0), (7, 0)), #Analisis complementarios
            ('SPAN', (1, 1), (4, 1)), #PH
            ('SPAN', (5, 1), (7, 1)), #NEUTRALIZANTES
            ('SPAN', (0, 1), (0, 2)), #Puntos de evaluación
            ('SPAN', (1, 2), (1, 2)), #N
            ('SPAN', (2, 1), (4, 1)), #PROMEDIO
            ('SPAN', (4, 2), (4, 2)), #N
            ('SPAN', (6, 1), (7, 1)), #POSITIVO
        ]))

        tabla_ph._argW = [90, 30, 30, 30, 30, 30, 30, 30]
        #Tabla de pH - Fin
        
        #Tabla de observaciones - Inicio

        datos_observaciones_table= [
            ['Observaciones', ''],
            ['Folio', 'Observaciones'],
        ]

        #Datos de observaciones


        tabla_observaciones = Table(datos_observaciones_table)
        tabla_observaciones.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ('SPAN', (0, 0), (1, 0)),  # Fusionar la primera fila
        ]))
        # Asignar los anchos de las columnas y las alturas de las filas
        tabla_observaciones._argW = [60, 662]
        #Tabla de observaciones - Fin


        #Tabla contenedoras de 
        tabla_contenedora_contenido= Table([
            [tabla_produccion, tabla_envasado, tabla_peso_envase_vacio],
        ])

        tabla_contenedora_contenido.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),   # Alinear la primera columna a la izquierda
            ('ALIGN', (1, 0), (1, 0), 'CENTER'), # Alinear la segunda columna al centro
            ('ALIGN', (2, 0), (2, 0), 'RIGHT'),  # Alinear la tercera columna a la derecha
            ('VALIGN', (0, 0), (-1, -1), 'TOP'), # Alinear verticalmente la tabla a la parte superior
            ('LEFTPADDING', (0, 0), (-1, -1), 0),# Eliminar padding a la izquierda para alinear al máximo
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),# Eliminar padding a la derecha
            ('TOPPADDING', (0, 0), (-1, -1), 0), # Eliminar padding en la parte superior
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0)# Eliminar padding en la parte inferior
        ]))


        tabla_contenedora_contenido._argW = [239, 245, 239]

        tabla_contenedora_contenido2 = Table([
            [tabla_microbiologicos, tabla_ph],
        ])

        tabla_contenedora_contenido2.setStyle(TableStyle([
            ('ALIGN', (0, 0), (0, 0), 'LEFT'),   # Alinear la primera columna a la izquierda
            ('ALIGN', (1, 0), (1, 0), 'RIGHT'),  # Alinear la tercera columna a la derecha
            ('VALIGN', (0, 0), (-1, -1), 'TOP'), # Alinear verticalmente la tabla a la parte superior
            ('LEFTPADDING', (0, 0), (-1, -1), 0),# Eliminar padding a la izquierda para alinear al máximo
            ('RIGHTPADDING', (0, 0), (-1, -1), 0),# Eliminar padding a la derecha
            ('TOPPADDING', (0, 0), (-1, -1), 0), # Eliminar padding en la parte superior
            ('BOTTOMPADDING', (0, 0), (-1, -1), 0)# Eliminar padding en la parte inferior
        ]))
        
        tabla_contenedora_contenido2._argW = [361, 361]

        elementos = [
            tabla_contenedora_encabezado, Spacer(0, 10),
            tabla_fisicoquimica, Spacer(0, 10),
            tabla_contenedora_contenido, Spacer(0, 10),
            tabla_contenedora_contenido2, Spacer(0, 10),
            tabla_observaciones, Spacer(0, 10),
        ]
        doc.build(elementos)
        return response


class ReporteRX50(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        fecha_inicial = request.GET.get('fecha-inicial')
        fecha_final = request.GET.get('fecha-final')
        producto = request.GET.get('producto')

        # Inicializa rango_fechas y rango_folios como None
        rango_fechas = None
        rango_folios = None
        
        # Si se proporcionan fechas y tipo de producto, filtrar en consecuencia
        if fecha_inicial and fecha_final and producto:
            if producto == "todos":
                silos_datos = LecheReconsSilos.objects.filter(
                    fecha_Hora__range=[fecha_inicial, fecha_final]
                )
            else:
                silos_datos = LecheReconsSilos.objects.filter(
                    fecha_Hora__range=[fecha_inicial, fecha_final],
                    producto=producto
                )
            encabezado_datos = LecheReconsSilosEncab.objects.filter(
                lechereconssilos__in=silos_datos
            ).distinct()

            rango_fechas = LecheReconsSilos.objects.filter(
                fecha_Hora__range=[fecha_inicial, fecha_final]
            ).aggregate(
                fecha_inicial=Min('fecha_Hora'),
                fecha_final=Max('fecha_Hora')
            )
            
            rango_folios = LecheReconsSilosEncab.objects.filter(
                lechereconssilos__in=silos_datos
            ).aggregate(
                folio_inicial=Min('folio'),
                folio_final=Max('folio')
            )

        else:
            # Usar el pk para obtener los datos de encabezado y el detalle de los silos
            encabezado_datos = LecheReconsSilosEncab.objects.filter(pk=pk)
            silos_datos = LecheReconsSilos.objects.filter(encabezado=pk)


        # Calcular las fórmulas globales
        formulas_globales = silos_datos.aggregate(
            numero_muestras=Count('id'),
            sum_Volumen=Sum('volumen'),
            temperatura_Promedio=Sum(F('volumen') * F('temperatura'), output_field=FloatField()) / Sum('volumen'),
            densidad_Promedio=Sum(F('volumen') * F('densidad'), output_field=FloatField()) / Sum('volumen'),
            s_g_w_v_Promedio=Sum(F('volumen') * F('s_g_w_v'), output_field=FloatField()) / Sum('volumen'),
            s_n_g_Stsg_wv_Promedio=Sum(F('volumen') * F('s_n_g_Stsg_wv'), output_field=FloatField()) / Sum('volumen'),
            proteina_Promedio=Sum(F('volumen') * F('proteina'), output_field=FloatField()) / Sum('volumen'),
        )
        
        # Calcular las fórmulas por tipo de producto si se seleccionó "Todos"
        formulas_por_producto = {}
        tipos_productos = Producto.objects.all()  # Obtener todos los tipos de producto
        for tipo_producto in tipos_productos:
            datos_producto = silos_datos.filter(producto=tipo_producto)
            formulas_producto = datos_producto.aggregate(
                numero_muestras=Count('id'),
                sum_Volumen=Sum('volumen'),
                temperatura_Promedio=Sum(F('volumen') * F('temperatura'), output_field=FloatField()) / Sum('volumen'),
                densidad_Promedio=Sum(F('volumen') * F('densidad'), output_field=FloatField()) / Sum('volumen'),
                s_g_w_v_Promedio=Sum(F('volumen') * F('s_g_w_v'), output_field=FloatField()) / Sum('volumen'),
                s_n_g_Stsg_wv_Promedio=Sum(F('volumen') * F('s_n_g_Stsg_wv'), output_field=FloatField()) / Sum('volumen'),
                proteina_Promedio=Sum(F('volumen') * F('proteina'), output_field=FloatField()) / Sum('volumen'),
                )
            formulas_por_producto[tipo_producto.nombre] = formulas_producto

      
        context = {
            'encabezado_datos': encabezado_datos.order_by('folio'),
            'datos': silos_datos.order_by('encabezado'),
            'producto_seleccionado': producto,
            'formulas_globales': formulas_globales,
            'formulas_por_producto': formulas_por_producto,
            }
        
        if rango_fechas:
            context['rango_fechas'] = rango_fechas
        if rango_folios:
            context['rango_folios'] = rango_folios

        return render(request, 'reporte_Rx50.html', context)


class ReporteRX51(View):

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        fecha_inicial = request.GET.get('fecha-inicial')
        fecha_final = request.GET.get('fecha-final')
        producto = request.GET.get('producto')

        # Inicializa rango_fechas y rango_folios como None
        rango_fechas = None
        rango_folios = None
        
        # Si se proporcionan fechas y tipo de producto, filtrar en consecuencia
        if fecha_inicial and fecha_final and producto:
            if producto == "todos":
                encabezado_datos = terminadoEncab.objects.filter(
                    fecha__range=[fecha_inicial, fecha_final]
                )
            else:
                encabezado_datos = terminadoEncab.objects.filter(
                    fecha__range=[fecha_inicial, fecha_final],
                    producto_terminado__producto=producto
                ).distinct()

            terminado_datos = producto_terminado.objects.filter(
                encabezado__in=encabezado_datos
            )

            rango_fechas = encabezado_datos.aggregate(
                fecha_inicial=Min('fecha'),
                fecha_final=Max('fecha')
            )

            rango_folios = encabezado_datos.aggregate(
                folio_inicial=Min('folio'),
                folio_final=Max('folio')
            )

        else:
            # Usar el pk para obtener los datos de encabezado y el detalle de los silos
            encabezado_datos = terminadoEncab.objects.filter(pk=pk)
            terminado_datos = producto_terminado.objects.filter(encabezado=pk)

        # Calcular las fórmulas globales
        formulas_globales = terminado_datos.aggregate( 
            numero_muestras=Count('id'),
            sum_Volumen=Sum('volumen'),
            temperatura_Promedio=Sum(F('volumen') * F('temperatura'), output_field=FloatField()) / Sum('volumen'),
            densidad_Promedio=Sum(F('volumen') * F('densidad'), output_field=FloatField()) / Sum('volumen'),
            s_g_w_v_Promedio=Sum(F('volumen') * F('sg'), output_field=FloatField()) / Sum('volumen'),
            s_n_g_Stsg_wv_Promedio=Sum(F('volumen') * F('sng'), output_field=FloatField()) / Sum('volumen'),
            proteina_Promedio=Sum(F('volumen') * F('proteina'), output_field=FloatField()) / Sum('volumen'),
        )

        # Calcular las fórmulas por tipo de producto si se seleccionó "Todos"
        formulas_por_producto = {}
        tipos_productos = Producto.objects.all()  # Obtener todos los tipos de producto
        for tipo_producto in tipos_productos:
            datos_producto = terminado_datos.filter(producto=tipo_producto)
            formulas_producto = datos_producto.aggregate(
                numero_muestras=Count('id'),
                sum_Volumen=Sum('volumen'),
                temperatura_Promedio=Sum(F('volumen') * F('temperatura'), output_field=FloatField()) / Sum('volumen'),
                densidad_Promedio=Sum(F('volumen') * F('densidad'), output_field=FloatField()) / Sum('volumen'),
                s_g_w_v_Promedio=Sum(F('volumen') * F('sg'), output_field=FloatField()) / Sum('volumen'),
                s_n_g_Stsg_wv_Promedio=Sum(F('volumen') * F('sng'), output_field=FloatField()) / Sum('volumen'),
                proteina_Promedio=Sum(F('volumen') * F('proteina'), output_field=FloatField()) / Sum('volumen'),
            )
            formulas_por_producto[tipo_producto.nombre] = formulas_producto

        context = {
            'encabezado_datos': encabezado_datos.order_by('folio'),
            'datos': terminado_datos.order_by('encabezado'),
            'producto_seleccionado': producto,
            'formulas_globales': formulas_globales,
            'formulas_por_producto': formulas_por_producto,
        }

        if rango_fechas:
            context['rango_fechas'] = rango_fechas
        if rango_folios:
            context['rango_folios'] = rango_folios

        return render(request, 'reporte_Rx51.html', context)


    #START--CALCULOS PARA OBTENER PESO NETO -----------------------------------------------------|

class VolumenNetoView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk') # Asumiendo que el pk se pasa como un argumento en la URL
        
        # CALCULOS ENCABEZADO
        datosEncabezado = EncabTablaR49.objects.filter(pk=pk)
        calculosEncabezado = datosEncabezado.aggregate(
            #Aqui van las formulas modelo1

        )

        # START CALCULOS DENSIDAD----------------------------------------------------------------|
        datosDensidad = Densidadpt.objects.all()
        producto_sum = datosDensidad.aggregate(
            densidad_volumen_sum=Sum(F('densidad') * F('volumen'), output_field=DecimalField(max_digits=10, decimal_places=4))
        )

        # Calcular la suma de volumen
        volumen_sum = datosDensidad.aggregate(
            volumen_sum=Sum('volumen', output_field=DecimalField(max_digits=5, decimal_places=4))
        )

        # Dividir la suma del producto por la suma de volumen para obtener la densidad ponderada
        densidadPonderada = producto_sum['densidad_volumen_sum'] / volumen_sum['volumen_sum'] if volumen_sum['volumen_sum'] else None
        print(f'Densidad Ponderada: {densidadPonderada}')

        calculos2 = {
            'densidadPonderada': densidadPonderada
        }
        # END CALCULOS DENSIDAD----------------------------------------------------------------|

        #CALCULOS PESO BRUTO ----------------------------------------
        datosPesoBruto = Pesobruto.objects.filter(encabezado=pk)
        calculosPesoBruto = datosPesoBruto.aggregate(
            #Aqui van las formulas modelo3
        )

        #CALCULOS PESO ENVASE VACIO ----------------------------------------
        datosPesoEnvVacio = Pesoenvvacio.objects.all()
        calculosPesoEnvVacio = datosPesoEnvVacio.aggregate(
            #Aqui van las formulas modelo4
            pesoPromedio=Avg('peso'),
        )
        peso_promedio = calculosPesoEnvVacio["pesoPromedio"]
        if peso_promedio is not None:
             print(f'Peso Promedio: {peso_promedio}')
        else:
             print('No se pudo calcular el peso promedio.')
            

         # Renderizar a la plantilla con los datos calculados
        context = {
            'datosEncabezado': datosEncabezado,
            'datosDensidad': datosDensidad,
            'datosPesoBruto': datosPesoBruto,
            'datosPesoEnvVacio': datosPesoEnvVacio,
            'calculosEncabezado': calculosEncabezado,
            'calculosPesoEnvVacio': calculosPesoEnvVacio,
            'calculosPesoBruto':calculosPesoBruto,
            'calculos2':calculos2,
        } 
        return render(request, ['reporte_VolumenNetoR49.html','pesonetor49_list.html'], context)




#----START PRUEBAS USANDO JSON RESPONSE EN CALCULOS PESO NETO-------------------------------------------------|
class CalculosR49DataView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')  # Redirige a la página de login si no está autenticado

    def get(self, request, *args, **kwargs):
        # Calcular el peso promedio
        datosPesoEnvVacio = Pesoenvvacio.objects.all()
        calculosPesoEnvVacio = datosPesoEnvVacio.aggregate(
            pesoPromedio=Avg('peso'),
        )
        

        # Filtrar los datos para densidad ponderada
        datosDensidad = Densidadpt.objects.all()
        
        # Calcular la suma ponderada de densidad por volumen
        producto_sum = datosDensidad.aggregate(
            densidad_volumen_sum=Sum(F('densidad') * F('volumen'), output_field=DecimalField(max_digits=10, decimal_places=4))
        )

        # Calcular la suma de volumen
        volumen_sum = datosDensidad.aggregate(
            volumen_sum=Sum('volumen', output_field=DecimalField(max_digits=5, decimal_places=4))
        )

        # Dividir la suma del producto por la suma de volumen para obtener la densidad ponderada
        densidadPonderada = producto_sum['densidad_volumen_sum'] / volumen_sum['volumen_sum'] if volumen_sum['volumen_sum'] else None
        
        # Obtener los datos de Pesobruto
        datosPesoBruto = Pesobruto.objects.all()

        #Realizar el cálculo de peso neto y agregar datos importantes: cabezal, id, valor peso bruto para renderizar al temmplate
        resultadosPesoNeto = [
            { 
                'id': dato.id,
                'cabezal':dato.cabezal.nombre,
                'valorPesoBruto': dato.valor,
                'resultado': int((dato.valor - calculosPesoEnvVacio['pesoPromedio']) / densidadPonderada) if densidadPonderada else None
            }
            for dato in datosPesoBruto
        ]

        

        # Crear el diccionario de resultados para la respuesta JSON
        resultados = {
            'pesoPromedio': calculosPesoEnvVacio['pesoPromedio'],
            'densidadPonderada': densidadPonderada,
            'resultadosPesoNeto': resultadosPesoNeto   #agregado prueba resultado para peso neto
        }

        # Retornar la respuesta en formato JSON
        return JsonResponse(resultados)
    
#----END PRUEBAS USANDO JSON RESPONSE EN CALCULOS PESO NETO-----------------------------------------------|
        

#[--------------------------[START VISTA CALCULOS-R49-RANGOS DE FECHAS]--------------------------------]

class ReporteR49RangoFechaView(LoginRequiredMixin, View):
    login_url = reverse_lazy('usuarios:login')  # Redirige a la página de login si no está autenticado

    def get(self, request, *args, **kwargs):
        return HttpResponse("Método GET no permitido en esta vista. Por favor, utiliza POST.", status=405)
    
    def post(self, request, *args, **kwargs):
        fecha_inicial = request.POST.get('fecha-inicial')
        fecha_final = request.POST.get('fecha-final')

        # Validar y parsear las fechas
        try:
            fecha_inicial = parse_date(fecha_inicial)
            fecha_final = parse_date(fecha_final)
        except ValueError:
            return JsonResponse({'error': 'Fechas inválidas'}, status=400)

        # Filtrar los datos por el rango de fechas
        datosPesoEnvVacio = Pesoenvvacio.objects.filter(fechaHora__date__range=[fecha_inicial, fecha_final])
        datosDensidad = Densidadpt.objects.filter(fechaHora__date__range=[fecha_inicial, fecha_final])
        datosPesoBruto = Pesobruto.objects.filter(fechaHora__date__range=[fecha_inicial, fecha_final])

        # Calcular el peso promedio y densidad ponderada
        calculosPesoEnvVacio = datosPesoEnvVacio.aggregate(
            pesoPromedio=Avg('peso'),
        )
        
        producto_sum = datosDensidad.aggregate(
            densidad_volumen_sum=Sum(F('densidad') * F('volumen'), output_field=DecimalField(max_digits=10, decimal_places=4))
        )
        
        volumen_sum = datosDensidad.aggregate(
            volumen_sum=Sum('volumen', output_field=DecimalField(max_digits=5, decimal_places=4))
        )
        
        densidadPonderada = producto_sum['densidad_volumen_sum'] / volumen_sum['volumen_sum'] if volumen_sum['volumen_sum'] else None

        # Calcular los resultados de peso neto en lugar de peso bruto
        resultadosPesoNeto = [
            {
                'valor': dato.valor,
                'id': dato.id,
                'cabezal': dato.cabezal.nombre,
                'resultado': int((dato.valor - calculosPesoEnvVacio['pesoPromedio']) / densidadPonderada) if densidadPonderada else None
            }
            for dato in datosPesoBruto
        ]

        # Cálculos para cada combinación de máquina y cabezal
        combinaciones = [
            ('1', 'A'),
            ('1', 'B'),
            ('2', 'C'),
            ('2', 'D'),
            ('3', 'E'),
            ('3', 'F')
        ]

        calculos_diarios = {}
        for maquina, cabezal in combinaciones:
            datos_maquina_cabezal = [dato for dato in resultadosPesoNeto if dato['cabezal'] == cabezal]

            if datos_maquina_cabezal:
                valores = [dato['resultado'] for dato in datos_maquina_cabezal if dato['resultado'] is not None]
                calculos_diarios[f"{maquina}-{cabezal}"] = {
                    'numero_Datos': len(valores),
                    'promedio': sum(valores) / len(valores) if valores else None,
                    'desviacion_Estandar': statistics.stdev(valores) if len(valores) > 1 else None,
                    'maximo': max(valores) if valores else None,
                    'minimo': min(valores) if valores else None,
                }
            else:
                calculos_diarios[f"{maquina}-{cabezal}"] = {
                    'numero_Datos': 0,
                    'desviacion_Estandar': None,
                    'maximo': None,
                    'minimo': None,
                }

        # Cálculos semanales
        total_datos_semanales = len(resultadosPesoNeto)
        valores_ponderados = [dato['resultado'] for dato in resultadosPesoNeto if dato['resultado'] is not None]

        promedio_total_ponderado = sum(valores_ponderados) / total_datos_semanales if total_datos_semanales else None
        desviacion_total_ponderada = statistics.stdev(valores_ponderados) if len(valores_ponderados) > 1 else None
        maximo_semanal = max(valores_ponderados) if valores_ponderados else None
        minimo_semanal = min(valores_ponderados) if valores_ponderados else None

        # Peso promedio
        pesoPromedio = calculosPesoEnvVacio['pesoPromedio']

        # Generar el JSON de resultados
        resultadosporfecha = {
            'diarios': calculos_diarios,
            'semanales': {
                'total_Datos': total_datos_semanales,
                'promedio_Total_Ponderado': promedio_total_ponderado,
                'desviacion_Total_Ponderada': desviacion_total_ponderada,
                'maximo_Semanal': maximo_semanal,
                'minimo_Semanal': minimo_semanal,
                'densidadPonderada': densidadPonderada,
                'pesoPromedio': pesoPromedio,
            },
        }

        return JsonResponse(resultadosporfecha)

    
class MostrarDiarioSemanalView(LoginRequiredMixin, TemplateView):
    # model = Pesobruto  #borrar locomentado si no hay errores
    # queryset = Pesobruto.objects.all()
    template_name = 'reporte_R49_DiarioSemanal.html'
    login_url = reverse_lazy('usuarios:login')