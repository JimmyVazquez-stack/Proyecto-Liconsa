from django.db.models import Avg, Min, Max, Count
from django.shortcuts import render
from django.views import View
from .models import ModeloTemporal

# Create your views here.
from django.db.models import Avg, Min, Max, Count, Sum, F, DecimalField
from django.shortcuts import render
from django.views import View
from .models import ModeloTemporal
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
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






# START PRUEBAS USANDO JSON RESPONSE EN CALCULOS DENSIDAD------------------------------------------|
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

        #Realizar el cálculo de peso neto
        resultadosPesoNeto = [
            {
                
                'valor': dato.valor,
                'resultado': (dato.valor - calculosPesoEnvVacio['pesoPromedio']) / densidadPonderada if densidadPonderada else None
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
    

# END PRUEBAS USANDO JSON RESPONSE EN CALCULOS DENSIDAD------------------------------------------|