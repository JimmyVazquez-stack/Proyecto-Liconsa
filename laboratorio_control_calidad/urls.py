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

    #Rutas para el CRUD de FormatoR49
    path('registror49_create/', registror49_create.as_view(), name='registror49_create'),
    path('registror49_list/', registror49_list.as_view(), name='registror49_list'),
    path('registror49_delete/<int:pk>', registror49_delete.as_view(), name='registror49_delete'),
    path('registror49_update/<int:pk>', registror49_update.as_view(), name='registror49_update'),
    #complementarias Densidad
    path('densidadr49_create/', densidadr49_create.as_view(), name='densidadr49_create'),
    path('densidadr49_list/', densidadr49_list.as_view(), name='densidadr49_list'),
    path('densidadr49_delete/<int:pk>', densidadr49_delete.as_view(), name='densidadr49_delete'),
    path('densidadr49_update/<int:pk>', densidadr49_update.as_view(), name='densidadr49_update'),
    #complementarias Peso vacio
    path('pesoenvvacior49_create/', pesoenvvacior49_create.as_view(), name='pesoenvvacior49_create'),
    path('pesoenvvacior49_list/', pesoenvvacior49_list.as_view(), name='pesoenvvacior49_list'),
    path('pesoenvvacior49_delete/<int:pk>', pesoenvvacior49_delete.as_view(), name='pesoenvvacior49_delete'),
    path('pesoenvvacior49_update/<int:pk>', pesoenvvacior49_update.as_view(), name='pesoenvvacior49_update'),
    #complementarias Peso bruto
    path('pesobrutor49_create/', pesobrutor49_create.as_view(), name='pesobrutor49_create'),
    path('pesobrutor49_list/', pesobrutor49_list.as_view(), name='pesobrutor49_list'),
    path('pesobrutor49_delete/<int:pk>', pesobrutor49_delete.as_view(), name='pesobrutor49_delete'),
    path('pesobrutor49_update/<int:pk>', pesobrutor49_update.as_view(), name='pesobrutor49_update'),
    # - [Start] - rutas para el CRUD de LecheReconstituidaPorSilosEncab - [Start] - #

    path('Leche_Reconstituida_Por_Silos_Encab/list', LecheReconsSilosEncabView.as_view(), name='Leche_Recons_Silos_Encab_List'),
    path('Leche_Reconstituida_Por_Silos_Encab/create', LecheReconsSilosEncabCreate.as_view(), name='Leche_Recons_Silos_Encab_Create'),
    path('Leche_Reconstituida_Por_Silos_Encab/delete/<int:pk>', LecheReconsSilosEncabDelete.as_view(), name='Leche_Recons_Silos_Encab_Delete'),
    path('Leche_Reconstituida_Por_Silos_Encab/update/<int:pk>', LecheReconsSilosEncabUpdate.as_view(), name='Leche_Recons_Silos_Encab_Update'),
    
    # - [End] - rutas para el CRUD de LecheReconstituidaPorSilos - [End] - #


    path('producto_terminadoList/', TerminadoEncabView.as_view(), name='TerminadoList'),
    path('producto_terminadoCreate/', TerminadoEncabCreate.as_view(), name='producto_terminadoCreate'),
    path('encab_update/<int:pk>',TerminadoEncabUpdate.as_view(), name='encab_update'),
    path('Terminado_delete/<int:pk>', TerminadoDelete.as_view(), name='Terminado_delete'),
    path('permisos/<int:pk>', permisos.as_view(), name='permisos'),
    path('modificar/<int:pk>', permisos.as_view(), name='modificar'),
]
  
