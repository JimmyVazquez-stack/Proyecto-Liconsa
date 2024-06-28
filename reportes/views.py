from django.db.models import Avg, Min, Max, Count
from django.shortcuts import render
from django.views import View
from django.db.models import Count, Avg, Min, Max
from .models import ComposicionFisioquimica, PuntosDeEvaluacion

class ReporteMensualView(View):
    def get(self, request, *args, **kwargs):
        # Obtén todos los productos
        productos = PuntosDeEvaluacion.objects.all()

        # Calcula las métricas para cada producto
        datos = []
        for producto in productos:
            metricas_producto = ComposicionFisioquimica.objects.filter(nombre=producto).aggregate(
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
            # Agrega el nombre del producto a las métricas
            metricas_producto['nombre'] = producto.nombre
            datos.append(metricas_producto)

        # Pasa los datos a tu plantilla
        context = {
            'datos': datos,
        }
        return render(request, 'reporte_mensual.html', context)