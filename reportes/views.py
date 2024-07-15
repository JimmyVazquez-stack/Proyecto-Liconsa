from django.http import HttpResponse
from django.views.generic import View
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Frame, PageTemplate
from reportlab.lib import colors
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
from reportlab.lib.pagesizes import letter
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg
from reportlab.pdfgen.canvas import Canvas
import os
from django.db.models import Avg, Min, Max, Count, Sum, F, FloatField
from django.shortcuts import render
from django.views import View

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
            renderPDF.draw(drawing, canvas, 0, 500)  # Dibuja en la posición ajustada y escalada

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

        # Añadir la plantilla de página con el encabezado
        frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 1 * doc.bottomMargin, id='normal')
        template = PageTemplate(id='header_template', frames=frame, onPage=header)
        doc.addPageTemplates([template])

        # Función para manejar valores None
        def safe_value(value, default="N/A"):
            return default if value is None else value
            # Datos y tablas como lo tienes actualmente
               
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
            ('SPAN', (2,2), (5,2)), #g/ml
            ('SPAN', (6,2), (9,2)), #g/ml
            ('SPAN', (10,2), (13,2)), #g/ml
            ('SPAN', (14,2), (17,2)), #g/ml
            ('SPAN', (18,2), (21,2)), #centigrados
            ('SPAN', (0, 1), (0, 3)),  # Punto de evaluación
            ('SPAN', (1, 1), (1, 3)),  # Numero de muestras
            ('WORDWRAP', (0, 0), (-1, -1)),  # Habilitar ajuste de línea
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Alinear verticalmente en el medio
            ('LEFTPADDING', (0, 0), (-1, -1), 5),  # Padding izquierdo
            ('RIGHTPADDING', (0, 0), (-1, -1), 5),  # Padding derecho
            
        ]))

        # Posicionar la tabla
        # Ajusta 'x_position' y 'y_position' según donde quieras colocar la tabla
        x_position = doc.leftMargin
        y_position = text_y_position - 100  # Por ejemplo, 100 puntos por debajo del texto del encabezado

        table.wrapOn(canvas, doc.width - 2 * doc.leftMargin, doc.bottomMargin)
        table.drawOn(canvas, x_position, y_position)

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




from laboratorio_control_calidad.models import *
from catalogos.models import *



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

