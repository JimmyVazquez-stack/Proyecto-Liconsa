from django.db.models import Avg, Min, Max, Count
from django.shortcuts import render
from django.views import View
from .models import ModeloTemporal

# Create your views here.
from django.db.models import Avg, Min, Max, Count, Sum, F, DecimalField
from django.shortcuts import render
from django.views import View
from .models import ModeloTemporal
from laboratorio_control_calidad.models import Densidadpt, Pesoenvvacio, Pesobruto, EncabTablaR49

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
    




    #START--CALCULOS PARA OBTENER PESO NETO -----------------------------------------------------|

class VolumenNetoView(View):
    def get(self, request, *args, **kwargs):
        pk = kwargs.get('pk') # Asumiendo que el pk se pasa como un argumento en la URL
        
        
        
        # CALCULOS ENCABEZADO
        datosEncabezado = EncabTablaR49.objects.filter(pk=pk)
        calculosEncabezado = datosEncabezado.aggregate(
            #Aqui van las formulas modelo1

        )

        # CALCULOS DENSIDAD
        datosDensidad = Densidadpt.objects.all()
        producto_sum = datosDensidad.aggregate(
            densidad_volumen_sum=Sum(F('densidad') * F('volumen'), output_field=DecimalField(max_digits=10, decimal_places=4))
        )

        # Calcular la suma de volumen
        volumen_sum = datosDensidad.aggregate(
            volumen_sum=Sum('volumen', output_field=DecimalField(max_digits=10, decimal_places=4))
        )

        # Dividir la suma del producto por la suma de volumen para obtener la densidad ponderada
        densidadPonderada = producto_sum['densidad_volumen_sum'] / volumen_sum['volumen_sum'] if volumen_sum['volumen_sum'] else None

        calculos2 = {
            'densidadPonderada': densidadPonderada
        }


        #CALCULOS PESO BRUTO ----------------------------------------
        datosPesoBruto = Pesobruto.objects.filter(encabezado=pk)
        calculosPesoBruto = datosPesoBruto.aggregate(
            #Aqui van las formulas modelo3
        )

        #CALCULOS PESO ENVASE VACIO ----------------------------------------
        datosPesoEnvVacio = Pesoenvvacio.objects.filter(encabezado=pk)
        calculosPesoEnvVacio = datosPesoEnvVacio.aggregate(
            #Aqui van las formulas modelo4
            pesoPromedio=Avg('peso'),
        )

        """
        calculosPesoEnVacio = datosPesoEnvVacio.aggregate(
              pesoPromedio=Avg('peso'),
        )
     
        # Calcular la suma del producto de densidad y volumen
        producto_sum = datosDensidad.aggregate(
            densidad_volumen_sum=Sum(F('densidad') * F('volumen'), output_field=DecimalField(max_digits=5, decimal_places=4))
        )
        # Calcular la suma de volumen
        volumen_sum = datosDensidad.aggregate(
            volumen_sum=Sum('volumen', output_field=DecimalField(max_digits=10, decimal_places=4))
        )
        # Dividir la suma del producto por la suma de volumen para obtener la densidad ponderada
        densidad_ponderada = producto_sum['densidad_volumen_sum'] / volumen_sum['volumen_sum'] if volumen_sum['volumen_sum'] else None

        calculos2 = {
            'densidadPonderada': densidad_ponderada
        }

        # Calcular el peso neto
        if densidad_ponderada != 0:
            peso_neto = (valor_peso_bruto - promedio_envase_vacio) / densidad_ponderada
        else:
            peso_neto = 0  # Manejar el caso donde la densidad ponderada es cero

        # Obtener el valor del peso bruto
        peso_bruto = get_object_or_404(Pesobruto, pk=6)
        valor_peso_bruto = peso_bruto.valor
        

        #calculos2 = datosDensidad.aggregate(
         #     densidadPonderada= Sum(F('densidad')* Decimal('volumen'), output_field=DecimalField(max_digits=5, decimal_places=4)/ Sum('volumen')),
        #)
        
         # Obtener el valor del peso bruto
        """


         # Renderizar a la plantilla con los datos calculados
        context = {
            'datosEncabezado': datosEncabezado,
            'datosDensidad': datosDensidad,
            'datosPesoBruto': datosPesoBruto,
            'datosPesoEnvVacio': datosPesoEnvVacio,
            'calculosEncabezado': calculosEncabezado, 
            **calculos2,
        } 
        return render(request, 'reporte_VolumenNetoR49.html', context)