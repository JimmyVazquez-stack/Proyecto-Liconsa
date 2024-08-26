from django.http import HttpResponse, JsonResponse
from django.views.generic import View, TemplateView
import os
from django.db.models import Min, Max, Count, Sum, F, FloatField, DecimalField, Avg, StdDev
from django.shortcuts import render
from django.views import View
from laboratorio_control_calidad.models import *
from catalogos.models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from laboratorio_control_calidad.models import LecheReconsSilos, Pesoenvvacio,Densidadpt, Pesobruto
from django.conf import settings
import requests
from django.shortcuts import render
from django.http import HttpResponse
from django.urls  import reverse_lazy
import statistics
from django.utils.dateparse import parse_date

#Importaciones de REPORTLAB
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Frame, PageTemplate
from reportlab.lib import colors
from reportlab.graphics import renderPDF
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
#APIS REST
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from laboratorio_control_calidad.models import LecheReconsSilos
from .serializers import LecheReconsSilosSerializer
from django.core.exceptions import ValidationError




#Vista para el reporte mensual para el laboratorio de control de calidad
class ReporteMensualView(LoginRequiredMixin, TemplateView):
        def get(self, request, *args, **kwargs):
            fecha_inicio = request.GET.get('fecha_inicio')
            fecha_fin = request.GET.get('fecha_fin')
            datos = []

            if fecha_inicio and fecha_fin:
                api_url = f"{settings.API_BASE_URL}api/composicion_fisicoquimica/?fecha_inicio={fecha_inicio}&fecha_fin={fecha_fin}"
                
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
            }
            print(context)
            return render(request, 'reporte_mensual.html', context)


#Vista para la API de composición fisicoquímica
class ComposicionFisicoquimicaDataView(APIView):
    def get(self, request, *args, **kwargs):
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')

        if not fecha_inicio or not fecha_fin:
            return Response({"error": "Se requieren ambos parámetros 'fecha_inicio' y 'fecha_fin' en el formato 'YYYY-MM-DD'"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            fecha_inicio = parse_date(fecha_inicio)
            fecha_fin = parse_date(fecha_fin)
            
            if fecha_inicio is None or fecha_fin is None:
                raise ValidationError("Formato de fecha incorrecto. Use 'YYYY-MM-DD'.")
            
            datos = LecheReconsSilos.objects.filter(fecha_Hora__date__range=[fecha_inicio, fecha_fin])
        except ValidationError:
            return Response({"error": "Formato de fecha incorrecto. Use 'YYYY-MM-DD'"}, status=status.HTTP_400_BAD_REQUEST)
        except ValueError:
            return Response({"error": "Error en el rango de fechas."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = LecheReconsSilosSerializer(datos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class PDFGeneratorView(View):
    def get(self, request, *args, **kwargs):
        # Crear la respuesta del HttpResponse con el tipo de contenido correcto
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="reporte.pdf"'

        # Crear el objeto PDF
        doc = SimpleDocTemplate(response, pagesize=landscape(A4))

        # Estilos para el PDF
        styles = getSampleStyleSheet()
        small_style = ParagraphStyle(name='Small', fontSize=8)

        def header(canvas, doc):
            canvas.saveState()

            # Ruta de la imagen SVG (asegúrate de que esta ruta sea válida)
            svg_path = "static/img/Liconsa.svg"

            # Verificar si el archivo SVG existe
            if not os.path.exists(svg_path):
                raise FileNotFoundError(f"El archivo SVG en la ruta {svg_path} no existe.")
            
            # Cargar el archivo SVG
            drawing = svg2rlg(svg_path)

            if drawing is None:
                raise ValueError(f"El archivo SVG en la ruta {svg_path} no se pudo cargar correctamente.")
            
            # Calcular el factor de escala para un tamaño deseado de 100x15 píxeles
            desired_width = 100  # Tamaño deseado en puntos
            desired_height = 15  # Tamaño deseado en puntos
            scale_width = desired_width / drawing.width
            scale_height = desired_height / drawing.height

            # Posicionar el SVG en el encabezado
            x_position = doc.leftMargin + 600  # Ajustar según tus necesidades
            y_position = doc.height + doc.topMargin - (desired_height)  # Ajustar según tus necesidades

            # Aplicar la transformación de escala y renderizar el SVG
            canvas.translate(x_position, y_position)
            canvas.scale(scale_width, scale_height)
            renderPDF.draw(drawing, canvas, 0, 0)  # Dibuja en la posición ajustada y escalada

            # Restablecer la transformación antes de dibujar el texto
            canvas.restoreState()
            canvas.saveState()

            # Encabezado de texto
            header_text = Paragraph("Reporte de Composición Fisicoquímica", styles['Heading1'])

            # Posicionar el texto del encabezado
            text_x_position = doc.leftMargin  # Ajustar para que el texto no se solape con el SVG
            text_y_position = doc.height + doc.topMargin - 10  # Ajustar la posición vertical según sea necesario

            header_text.wrapOn(canvas, doc.width - 10, doc.topMargin)
            header_text.drawOn(canvas, text_x_position, text_y_position)

            canvas.restoreState()

            # Retornar la posición Y del texto del encabezado
            return text_y_position

        # Añadir la plantilla de página con el encabezado
        frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - .5 * doc.bottomMargin, id='normal')
        template = PageTemplate(id='header_template', frames=frame, onPage=header)
        doc.addPageTemplates([template])

        # Función para manejar valores None
        def safe_value(value, default="N/A"):
            return default if value is None else value

        # Datos para el reporte
        punto_evaluacion = safe_value("Punto 1")
        numero_muestras = safe_value(10)
        densidad_promedio = safe_value(1.030)
        densidad_fle = safe_value(0.05)
        densidad_maximo = safe_value(1.035)
        densidad_minimo = safe_value(1.025)
        grasas_promedio = safe_value(3.5)
        grasas_fle = safe_value(0.1)
        grasas_maximo = safe_value(3.6)
        grasas_minimo = safe_value(3.4)
        sng_promedio = safe_value(8.5)
        sng_fle = safe_value(0.2)
        sng_maximo = safe_value(8.7)
        sng_minimo = safe_value(8.3)
        proteina_promedio = safe_value(3.2)
        proteina_fle = safe_value(0.1)
        proteina_maximo = safe_value(3.3)
        proteina_minimo = safe_value(3.1)
        temperatura_promedio = safe_value(4.0)
        temperatura_fle = safe_value(0.5)
        temperatura_maximo = safe_value(4.5)
        temperatura_minimo = safe_value(3.5)

        composicion_fisicoquimica_data = [
            ['Composicion Fisioquimica', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', ''],
            [Paragraph("Puntos de Evaluación", small_style), Paragraph("N", small_style), "Densidad", "", "", "", "Grasa", "", "", "", "SNG", "", "", "", "Proteínas", "", "", "", "Temperatura", "", "", ""],
            ["", "", "g/ml", "", "", "", "g/ml", "", "", "", "g/ml", "", "", "", "g/ml", "", "", "", "C°", "", "", ""],
            ["", "", "g/ml", "%FLE", "vMAX", "vMIN", "%", "%FLE", "vMAX", "vMIN", "%", "%FLE", "vMAX", "vMIN", "%", "%FLE", "vMAX", "vMIN", "°C", "%FLE", "vMAX", "vMIN"],
            [punto_evaluacion, numero_muestras, densidad_promedio, densidad_fle, densidad_maximo, densidad_minimo, grasas_promedio, grasas_fle, grasas_maximo, grasas_minimo, sng_promedio, sng_fle, sng_maximo, sng_minimo, proteina_promedio, proteina_fle, proteina_maximo, proteina_minimo, temperatura_promedio, temperatura_fle, temperatura_maximo, temperatura_minimo]
        ]

        # Crear la tabla
        tabla_fisicoquimica = Table(composicion_fisicoquimica_data)
        tabla_fisicoquimica.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
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
        tabla_fisicoquimica._argW = [40, 40] + [35]*20
        tabla_fisicoquimica._argH = [20] * 5

        datos_produccion = [
            ['Datos de producción', ''],
            ['Producción real', 'Producción ventas'],
            [safe_value(1000), safe_value(950)],
        ]

        tabla_produccion = Table(datos_produccion)
        tabla_produccion.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('SPAN', (0, 0), (1, 0)),  # Fusionar la primera fila
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
        ]))

        tabla_produccion._argW = [100, 100]
        tabla_produccion._argH = [20] * 3

        datos_envasado = [
            ['Control de envasado', '', '', '', '', ''],
            ['n', 'Contenido neto', '', '', '', ''],
            ['', 'ml', '', '', '', ''],
            ['', 'X', 'fli', 'CND-2T', 'máximo', 'mínimo'],
            [safe_value(100), safe_value(200), safe_value(1.5), safe_value(190), safe_value(210), safe_value(180)],
        ]

        tabla_envasado = Table(datos_envasado)
        tabla_envasado.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('SPAN', (0, 0), (5, 0)),  # Fusionar la primera fila  
            ('SPAN', (0, 1), (0, 3)),  # Fusionar la primera columna
            ('SPAN', (1, 1), (5, 1)),  # Fusionar la segunda columna
            ('SPAN', (1, 2), (5, 2)),  # Fusionar la tercera columna
        ]))

        datos_microbiologicos = [
            ['Calidad microbiológica', '', '', '', '', '', '', ''],
            ['Puntos de evaluación', 'N', 'Organismos coliformes', '', '', 'Aerobias', '', ''],
            ['', '', 'UFC/ml', '', '', 'UFC/ml', '', ''],
            ['', '', 'X', 'Fle', 'Máximo', 'X', 'Fle', 'Máximo'],
            [safe_value("Punto 1"), safe_value(10), safe_value(200), safe_value(20), safe_value(300), safe_value(400), safe_value(30), safe_value(500)],
        ]

        tabla_microbiologicos = Table(datos_microbiologicos)
        tabla_microbiologicos.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('SPAN', (0, 0), (7, 0)), #Calidad microbiológica
            ('SPAN', (2, 1), (4, 1)), #Organismos coliformes
            ('SPAN', (5, 1), (7, 1)), #Aerobias
            ('SPAN', (0, 1), (0, 3)), #Puntos de evaluación 
            ('SPAN', (1, 1), (1, 3)), #N
            ('SPAN', (2, 2), (4, 2)), #ufc/ml
            ('SPAN', (5, 2), (7, 2)), #ufc/ml
        ]))

        # Construir el documento
        elementos = [tabla_fisicoquimica, Spacer(1, 12), tabla_produccion, Spacer(1, 12), tabla_envasado, Spacer(1, 12), tabla_microbiologicos, Spacer(1, 12)]
        
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
        # Obtén los datos que quieres mostrar en el reporte
        pk = kwargs.get('pk')
        
        # Usar el pk para obtener los datos de encabezado y el detalle de los silos
        encabezado_datos = terminadoEncab.objects.filter(pk=pk)
        terminado_datos = producto_terminado.objects.filter(encabezado=pk)

        formulas = terminado_datos.aggregate(
            numero_muestras=Count('id'),
            sum_Volumen = Sum('volumen'),
            temperatura_Promedio = Sum(F('volumen') * F('temperatura'), output_field=FloatField()) / Sum('volumen'),
            densidad_Promedio = Sum(F('volumen') * F('temperatura'), output_field=FloatField()) / Sum('volumen'),
            s_g_Promedio = Sum(F('volumen') * F('sg'), output_field=FloatField()) / Sum('volumen'),
            s_n_g_Promedio = Sum(F('volumen') * F('sng'), output_field=FloatField()) / Sum('volumen'),
            proteina_Promedio = Sum(F('volumen') * F('proteina'), output_field=FloatField()) / Sum('volumen'),


        )
        # Pasa las métricas y los datos a tu plantilla
        context = {
            'encabezado_datos': encabezado_datos,
            'datos': terminado_datos,
            **formulas,
        }
        return render(request, 'reporte_mensual.html', context)
    

# class ReporteMensualView(View):
#     def get(self, request, *args, **kwargs):
#         # Obtén los datos que quieres mostrar en el reporte
#         datos = ModeloTemporal.objects.all()

#         metricas = datos.aggregate(
#             numero_muestras=Count('id'),
#             volumen_promedio=Avg('volumen'),
#             volumen_minimo=Min('volumen'),
#             volumen_maximo=Max('volumen'),

#             temperatura_promedio=Avg('temperatiura'),
#             temperatura_minimo=Min('temperatiura'),
#             temperatura_maximo=Max('temperatiura'),
            
#             densidad_promedio=Avg('densidadgml'),
#             densidad_minimo=Min('densidadgml'),
#             densidad_maximo=Max('densidadgml'),

#             grasas_promedio=Avg('grasasgl'),
#             grasas_minimo=Min('grasasgl'),
#             grasas_maximo=Max('grasasgl'),

#             sng_promedio=Avg('snggl'),
#             sng_minimo=Min('snggl'),
#             sng_maximo=Max('snggl'),

#             proteina_promedio=Avg('proteinagl'),
#             proteina_minimo=Min('proteinagl'),
#             proteina_maximo=Max('proteinagl'),

#             ph_promedio=Avg('ph'),
#             ph_minimo=Min('ph'),
#             ph_maximo=Max('ph'),
            
#         )

#         # Pasa las métricas y los datos a tu plantilla
#         context = {
#             'datos': datos,
#             **metricas,
#         }
#         return render(request, 'reporte_mensual.html', context)



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