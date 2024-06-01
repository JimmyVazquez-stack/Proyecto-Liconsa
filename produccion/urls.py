from django.urls import path
from .views import (index,
                    producto_silos,
                    leche_fluida_salida_pasteurizador,
                    leche_fluida_envase_litros,
                    verificacion_contenido_neto,
                    leche_cruda,
                    leche_frisia_pipa,
                    concentracion_soluciones_materiales_limpieza,)

app_name = 'produccion' 

urlpatterns = [
    path('', index.as_view(), name='index'),
    path('producto_silos/', producto_silos.as_view(), name='producto_silos'),
    path('leche_fluida_salida_pasteurizador/', leche_fluida_salida_pasteurizador.as_view(), name='leche_fluida_salida_pasteurizador'),
    path('leche_fluida_envase_litros/', leche_fluida_envase_litros.as_view(), name='leche_fluida_envase_litros'),
    path('verificacion_contenido_neto/', verificacion_contenido_neto.as_view(), name='verificacion_contenido_neto'),
    path('leche_cruda/', leche_cruda.as_view(), name='leche_cruda'),
    path('leche_frisia_pipa/', leche_frisia_pipa.as_view(), name='leche_frisia_pipa'),
    path('concentracion_soluciones_materiales_limpieza/', concentracion_soluciones_materiales_limpieza.as_view(), name='concentracion_soluciones_materiales_limpieza'),
]