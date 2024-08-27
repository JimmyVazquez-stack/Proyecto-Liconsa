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

    path('producto_terminadoList/', TerminadoEncabView.as_view(), name='TerminadoList'),
    path('producto_terminadoCreate/', TerminadoEncabCreate.as_view(), name='producto_terminadoCreate'),
    path('encab_update/<int:pk>',TerminadoEncabUpdate.as_view(), name='encab_update'),
    path('Terminado_delete/<int:pk>', TerminadoDelete.as_view(), name='Terminado_delete'),
    path('permisos/<int:pk>', permisos.as_view(), name='permisos'),
    path('modificar/<int:pk>', permisos.as_view(), name='modificar'),

    # PT 2.0 ENCAB-------------------------------------------
    path('pt_encabView', EncabView.as_view(), name='pt_encabView'),
    path('pt_encabCreate', EncabCreate.as_view(), name='pt_encabCreate'),     
    path('pt_encabUpdate/<int:pk>', EncabUpdate.as_view(), name='pt_encabUpdate'),
    
    # PT 2.0 ------------------------------------------------
    path('pt_View', TerminadoView.as_view(), name='pt_View'),
    path('pt_Create', TerminadoCreate.as_view(), name='pt_Create'),     
    path('pt_Update/<int:pk>', TerminadoUpdate.as_view(), name='pt_Update'),
    path('pt_Delete/<int:pk>', PTerminadoDelete.as_view(), name='pt_Delete'),

    #Juan Carlos URLS
        #Formato con encabezado
    # path('encabezador49V2_Create/', EncabR49CreateView.as_view(), name='encabezador49_create'),
    path('encabezador49V2_list/', EncabR49ListView.as_view(), name='encabezador49_list'),
    path('encabezador49V2_delete/<int:pk>/', EncabR49DeleteView.as_view(), name='encabezador49_delete'),
    path('encabezador49V2_update/<int:pk>/', EncabR49UpdateView.as_view(), name='encabezador49_update'),
        #Para valores de peso Neto
    path('pesonetor49_list/', MostrarPesosView.as_view(), name='pesonetor49_list'),
    #Rutas para el CRUD de FormatoR49 V2------------------------------------------------------
    path('densidadr49_Create/', Densidadr49CreateView.as_view(), name='densidadr49_Create'),
    path('densidadr49_List/', Densidadr49ListView.as_view(), name='densidadr49_List'),
    path('densidadr49_Delete/<int:pk>', Densidadr49DeleteView.as_view(), name='densidadr49_Delete'),
    path('densidadr49_Update/<int:pk>', Densidadr49UpdateView.as_view(), name='densidadr49_Update'),
    #complementarias Peso vacio
    path('pesoEnvVacior49_Create/', PesoEnvVacior49CreateView.as_view(), name='pesoEnvVacior49_Create'),
    path('pesoEnvVacior49_List/', PesoEnvVacior49ListView.as_view(), name='pesoEnvVacior49_List'),
    path('pesoEnvVacior49_Delete/<int:pk>', PesoEnvVacior49DeleteView.as_view(), name='pesoEnvVacior49_Delete'),
    path('pesoEnvVacior49_Update/<int:pk>', PesoEnvVacior49UpdateView.as_view(), name='pesoEnvVacior49_Update'),
    #complementarias Peso bruto
    path('pesoBrutor49_Create/', PesoBrutor49CreateView.as_view(), name='pesoBrutor49_Create'),
    path('pesoBrutor49_List/', PesoBrutor49ListView.as_view(), name='pesoBrutor49_List'),
    path('pesoBrutor49_Delete/<int:pk>', PesoBrutor49DeleteView.as_view(), name='pesoBrutor49_Delete'),
    path('pesoBrutor49_Update/<int:pk>', PesoBrutor49UpdateView.as_view(), name='pesoBrutor49_Update'),


    #Calidad microbiologica
    path('api/planta/', planta_list, name='planta_list'),
    path('api/producto/', producto_list, name='producto_list'),
    path('api/encabezados/', encabezados_list, name='encabezados_list_api'),      
    path('api/calidad-microbiologica/add/<int:encabezado_id>/', add_calidad_microbiologica, name='calidad_microbiologica_add'),
    path('api/calidad-microbiologica/', calidad_microbiologica_list, name='calidad_microbiologica_list'),
    path('api/calidad-microbiologica/edit/<int:pk>/', calidad_microbiologica_edit, name='calidad_microbiologica_edit'),
    path('api/calidad-microbiologica/update/', calidad_microbiologica_update, name='calidad_microbiologica_update'),    
    path('api/calidad-microbiologica/delete/<int:pk>/', calidad_microbiologica_delete, name='calidad_microbiologica_delete'),
    path('calidad-microbiologica/', CalidadMicrobiologicaView.as_view(), name='calidad_microbiologica'),
    path('calidad-microbiologica/update/<int:encabezado_id>/', CalidadMicrobiologicaView.as_view(), name='calidad_microbiologica_edit_encabezado'),
    path('calidad-microbiologica/delete/<int:encabezado_id>/', CalidadMicrobiologicaDeleteEncabezadoView.as_view(), name='calidad_microbiologica_delete_encabezado'),
    path('calidad-microbiologica/detalle/<int:encabezado_id>/', CalidadMicrobiologicaDetalleView.as_view(), name='calidad_microbiologica_detalle'),
    path('calidad-microbiologica/editar-encabezado/<int:pk>/', CalidadMicrobiologicaEncabezadoUpdateView.as_view(), name='calidad_microbiologica_editar_encabezado'),
]

