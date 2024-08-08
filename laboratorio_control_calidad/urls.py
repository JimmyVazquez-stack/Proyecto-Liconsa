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

       
    #Formato con encabezado
    # path('encabezador49_create/', Encabezador49Create.as_view(), name='encabezador49_create'),
    # path('encabezador49_list/', Encabezador49View.as_view(), name='encabezador49_list'),
    # path('encabezador49_delete/<int:pk>', Encabezador49Delete.as_view(), name='encabezador49_delete'),
    # path('encabezador49_update/<int:pk>', Encabezador49Update.as_view(), name='encabezador49_update'),
    
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


    #Formato con encabezado
    path('encabezador49V2_Create/', EncabR49CreateView.as_view(), name='encabezador49_create'),
    path('encabezador49V2_list/', EncabR49ListView.as_view(), name='encabezador49_list'),
    path('encabezador49V2_delete/<int:pk>', EncabR49DeleteView.as_view(), name='encabezador49_delete'),
    path('encabezador49V2_update/<int:pk>', EncabR49UpdateView.as_view(), name='encabezador49_update'),


]
    

