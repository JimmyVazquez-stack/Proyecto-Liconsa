from django.urls import path
from . import views

app_name = 'produccion' 

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('producto_silos/', views.producto_silos.as_view(), name='producto_silos'),
    path('leche_fluida_salida_pasteurizador/', views.leche_fluida_salida_pasteurizador.as_view(), name='leche_fluida_salida_pasteurizador'),
    path('leche_fluida_envase_litros/', views.leche_fluida_envase_litros.as_view(), name='leche_fluida_envase_litros'),
    path('verificacion_contenido_neto/', views.verificacion_contenido_neto.as_view(), name='verificacion_contenido_neto'),
    path('leche_cruda/', views.leche_cruda.as_view(), name='leche_cruda'),
    path('leche_frisia_pipa/', views.leche_frisia_pipa.as_view(), name='leche_frisia_pipa'),
    path('concentracion_soluciones_materiales_limpieza/', views.concentracion_soluciones_materiales_limpieza.as_view(), name='concentracion_soluciones_materiales_limpieza'),
]