from django.urls import path
from .views import *
app_name = 'laboratorio_control_calidad'

urlpatterns = [
    path('control_calidad/', index.as_view(), name='index'),
    path('grasas_aceites_vegetales/', grasas_aceites_vegetales.as_view(), name='grasas_aceites_vegetales'),
    path('mezcla_oleosa_vitaminas/', mezcla_oleosa_vitaminas.as_view(), name='mezcla_oleosa_vitaminas'),
    path('pre_mezclas_vitaminas_minerales/', pre_mezclas_vitaminas_minerales.as_view(), name='pre_mezclas_vitaminas_minerales'),
    path('leche_polvo_fysf', leche_polvo_fysf.as_view(), name='leche_polvo_fysf'),
    path('soluciones_valoradas_ts/', soluciones_valoradas_ts.as_view(), name='soluciones_valoradas_ts'),
    path('evaluacion_sensorial/', evaluacion_sensorial.as_view(), name='evaluacion_sensorial'),
    path('monitoreo_medio_ambiente/', monitoreo_medio_ambiente.as_view(), name='monitoreo_medio_ambiente'),
    path('limpieza_equipo_personal/', limpieza_equipo_personal.as_view(), name='limpieza_equipo_personal'),
    path('calibracion_verificacion_equipo/', calibracion_verificacion_equipo.as_view(), name='calibracion_verificacion_equipo'),    
    path('verificacion_documentos/', verificacion_documentos.as_view(), name='verificacion_documentos'),
    path('producto_terminadoList/', TerminadoEncabView.as_view(), name='TerminadoList'),
    path('producto_terminadoCreate/', TerminadoEncabCreate.as_view(), name='producto_terminadoCreate'),
    path('encab_update/<int:pk>',TerminadoEncabUpdate.as_view(), name='encab_update'),
    path('Terminado_delete/<int:pk>', TerminadoDelete.as_view(), name='Terminado_delete'),
    path('permisos/<int:pk>', permisos.as_view(), name='permisos'),
    path('modificar/<int:pk>', permisos.as_view(), name='modificar'),
]
  
