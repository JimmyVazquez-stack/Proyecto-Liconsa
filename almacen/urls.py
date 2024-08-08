from django.urls import path
from . import views

app_name = 'almacen' 

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('leche_polvo_fosf/', views.leche_polvo_fosf.as_view(), name='leche_polvo_fosf'),
    path('leche_cruda/', views.leche_cruda.as_view(), name='leche_cruda'),
    path('leche_frisia_pipa/', views.leche_frisia_pipa.as_view(), name='leche_frisia_pipa'),
    path('evaluacion_polietileno/', views.evaluacion_polietileno.as_view(), name='evaluacion_polietileno'),
    path('solucion_alcalina/', views.solucion_alcalina.as_view(), name='solucion_alcalina'),
    path('solucion_acida/', views.solucion_acida.as_view(), name='solucion_acida'),
    path('hipoclorito_sodio/', views.hipoclorito_sodio.as_view(), name='hipoclorito_sodio'),
]