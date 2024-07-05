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
    # path('registror49_create/', registror49_create.as_view(), name='registror49_create'),
    # path('registror49_list/', registror49_list.as_view(), name='registror49_list'),
    # path('registror49_delete/<int:pk>', registror49_delete.as_view(), name='registror49_delete'),
    # path('registror49_update/<int:pk>', registror49_update.as_view(), name='registror49_update'),
    #complementarias Densidad
    
    #Formato con encabezado
    path('encabezador49_create/', Encabezador49Create.as_view(), name='encabezador49_create'),
    path('encabezador49_list/', Encabezador49View.as_view(), name='encabezador49_list'),
    path('encabezador49_delete/<int:pk>', Encabezador49Delete.as_view(), name='encabezador49_delete'),
    path('encabezador49_update/<int:pk>', Encabezador49Update.as_view(), name='encabezador49_update'),

]
