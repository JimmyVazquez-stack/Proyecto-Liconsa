from django.db.models import Avg, Min, Max, Count, Sum, F, FloatField
from django.shortcuts import render
from django.views import View
from .models import ModeloTemporal

# Create your views here.
from django.db.models import Avg, Min, Max, Count
from django.shortcuts import render
from django.views import View
from .models import ModeloTemporal
from laboratorio_control_calidad.models import *

class ReporteMensualView(View):
    def get(self, request, *args, **kwargs):
        # Obtén los datos que quieres mostrar en el reporte
        datos = ModeloTemporal.objects.all()

        metricas = datos.aggregate(
            numero_muestras=Count('id'),
            volumen_promedio=Avg('volumen'),
            volumen_minimo=Min('volumen'),
            volumen_maximo=Max('volumen'),

            temperatura_promedio=Avg('temperatiura'),
            temperatura_minimo=Min('temperatiura'),
            temperatura_maximo=Max('temperatiura'),
            
            densidad_promedio=Avg('densidadgml'),
            densidad_minimo=Min('densidadgml'),
            densidad_maximo=Max('densidadgml'),

            grasas_promedio=Avg('grasasgl'),
            grasas_minimo=Min('grasasgl'), 
            grasas_maximo=Max('grasasgl'),

            sng_promedio=Avg('snggl'),
            sng_minimo=Min('snggl'),
            sng_maximo=Max('snggl'),

            proteina_promedio=Avg('proteinagl'),
            proteina_minimo=Min('proteinagl'),
            proteina_maximo=Max('proteinagl'),

            ph_promedio=Avg('ph'),
            ph_minimo=Min('ph'),
            ph_maximo=Max('ph'),
            
        )

        # Pasa las métricas y los datos a tu plantilla
        context = {
            'datos': datos,
            **metricas,
        }
        return render(request, 'reporte_mensual.html', context)
    
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

