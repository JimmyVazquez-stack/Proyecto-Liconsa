from django.urls import path
from .views import (index,
                    leche_polvo_fosf,
                    leche_cruda,
                    leche_frisia_pipa,
                    evaluacion_polietileno,
                    solucion_alcalina,
                    solucion_acida,
                    hipoclorito_sodio,)

app_name = 'almacen' 

urlpatterns = [
    path('', index.as_view(), name='index'),
    path('leche_polvo_fosf/', leche_polvo_fosf.as_view(), name='leche_polvo_fosf'),
    path('leche_cruda/', leche_cruda.as_view(), name='leche_cruda'),
    path('leche_frisia_pipa/', leche_frisia_pipa.as_view(), name='leche_frisia_pipa'),
    path('evaluacion_polietileno/', evaluacion_polietileno.as_view(), name='evaluacion_polietileno'),
    path('solucion_alcalina/', solucion_alcalina.as_view(), name='solucion_alcalina'),
    path('solucion_acida/', solucion_acida.as_view(), name='solucion_acida'),
    path('hipoclorito_sodio/', hipoclorito_sodio.as_view(), name='hipoclorito_sodio'),
]