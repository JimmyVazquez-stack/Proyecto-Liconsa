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
    


class ReporteRX50(View):

    def get(self, request, *args, **kwargs):
        # Obtén los datos que quieres mostrar en el reporte
        pk = kwargs.get('pk')

        # Usar el pk para obtener los datos de encabezado y el detalle de los silos
        encabezado_datos = LecheReconsSilosEncab.objects.filter(pk=pk)
        silos_datos = LecheReconsSilos.objects.filter(encabezado=pk)

        formulas = silos_datos.aggregate(
            numero_muestras=Count('id'),
            sum_Volumen = Sum('volumen'),
            temperatura_Promedio = Sum(F('volumen') * F('temperatura'), output_field=FloatField()) / Sum('volumen'),
            densidad_Promedio = Sum(F('volumen') * F('densidad'), output_field=FloatField()) / Sum('volumen'),
            s_g_w_v_Promedio = Sum(F('volumen') * F('s_g_w_v'), output_field=FloatField()) / Sum('volumen'),
            s_n_g_Stsg_wv_Promedio = Sum(F('volumen') * F('s_n_g_Stsg_wv'), output_field=FloatField()) / Sum('volumen'),
            proteina_Promedio = Sum(F('volumen') * F('proteina'), output_field=FloatField()) / Sum('volumen'),


        )
        # Pasa las métricas y los datos a tu plantilla
        context = {
            'encabezado_datos': encabezado_datos,
            'datos': silos_datos,
            **formulas,
        }
        return render(request, 'reporte_Rx50.html', context)