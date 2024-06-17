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

    # - [Start] - rutas para el CRUD de LecheReconstituidaPorSilosEncab - [Start] - #

    path('Leche_Reconstituida_Por_Silos_Encab/list', LecheReconsSilosEncabView.as_view(), name='Leche_Recons_Silos_Encab_List'),
    path('Leche_Reconstituida_Por_Silos_Encab/create', LecheReconsSilosEncabCreate.as_view(), name='Leche_Recons_Silos_Encab_Create'),
    path('Leche_Reconstituida_Por_Silos_Encab/delete/<int:pk>', LecheReconsSilosEncabDelete.as_view(), name='Leche_Recons_Silos_Encab_Delete'),
    path('Leche_Reconstituida_Por_Silos_Encab/update/<int:pk>', LecheReconsSilosEncabUpdate.as_view(), name='Leche_Recons_Silos_Encab_Update'),
    
    # - [End] - rutas para el CRUD de LecheReconstituidaPorSilos - [End] - #



     # - [Start] - rutas para el CRUD de LecheReconstituidaPorSilos - [Start] - #

    path('Leche_Reconstituida_Por_Silos/list', LecheReconsSilosView.as_view(), name='Leche_Recons_Silos_List'),
    path('Leche_Reconstituida_Por_Silos/create', LecheReconsSilosCreate.as_view(), name='Leche_Recons_Silos_Create'),
    path('Leche_Reconstituida_Por_Silos/delete/<int:pk>', LecheReconsSilosDelete.as_view(), name='Leche_Recons_Silos_Delete'),
    path('Leche_Reconstituida_Por_Silos/update/<int:pk>', LecheReconsSilosUpdate.as_view(), name='Leche_Recons_Silos_Update'),
    
    # - [End] - rutas para el CRUD de LecheReconstituidaPorSilos - [End] - #

]
