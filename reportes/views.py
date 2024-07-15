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



"""
from django.db.models import Avg, Min, Max, Count
from django.shortcuts import render
from django.views import View
from .models import ComposicionFisioquimica, PuntosDeEvaluacion
import datetime

class ReporteMensualView(View):
    def get(self, request, *args, **kwargs):
        # Define el mes y año para el reporte, por ejemplo, marzo de 2023
        año_reporte = 2023
        mes_reporte = 3

        # Calcula el primer momento del mes (inicio del día 1)
        inicio_mes = datetime.datetime(año_reporte, mes_reporte, 1)
        # Calcula el inicio del siguiente mes y resta un segundo para obtener el último momento del mes reportado
        fin_mes = datetime.datetime(año_reporte, mes_reporte + 1, 1) - datetime.timedelta(seconds=1)

        # Obtén todos los productos
        productos = PuntosDeEvaluacion.objects.all()

        # Calcula las métricas para cada producto dentro del rango de fechas y horas
        datos = []
        for producto in productos:
            metricas_producto = ComposicionFisioquimica.objects.filter(
                nombre=producto,
                fecha__range=(inicio_mes, fin_mes)  # Asume que `fecha` es el campo de fecha y hora en ComposicionFisioquimica
            ).aggregate(
                numero_muestras=Count('id'),
                volumen_promedio=Avg('volumen'),
                volumen_minimo=Min('volumen'),
                volumen_maximo=Max('volumen'),

                temperatura_promedio=Avg('temperatura'),  # Corrige el error tipográfico aquí
                temperatura_minimo=Min('temperatura'),
                temperatura_maximo=Max('temperatura'),
                
                densidad_promedio=Avg('densidadgml'),
                densidad_minimo=Min('densidadgml'),
                densidad_maximo=Max('densidadgml'),

                grasas_promedio=Avg('grasasgl'),
                grasas_minimo=Min('grasasgl'),
                grasas_maximo=Max('grasasgl'),

                # Continúa con el resto de tus métricas...
            )
            datos.append(metricas_producto)
        
        # Renderiza tus datos como necesites
        return render(request, 'tu_template.html', {'datos': datos})
"""