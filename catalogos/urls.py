from django.urls import path
from .views import (
    LecheriaListView, 
    AñadirLecheriaView, 
    LecheriaDataView, 
    ActualizarLecheriaView, 
    PoblacionListView, 
    AreaListView, 
    MaquinaListView, 
    CabezalListView, 
    PlantaListView, 
    ProveedorListView,
    SiloListView,
    TurnoListView,
    )

app_name = 'catalogos'

urlpatterns = [
    path('lecherias/list/', LecheriaListView.as_view(), name='lecherias_list'),
    path('añadir_lecheria/', AñadirLecheriaView.as_view(), name='añadir_lecheria'),
    path('lecherias/list/data/', LecheriaDataView.as_view(), name='lecherias_data'),
    path('actualizar_lecheria/', ActualizarLecheriaView.as_view(), name='actualizar_lecheria'),
    #rutas a poblaciones
    path('poblaciones/list/', PoblacionListView.as_view(), name='poblaciones_list'),
    #rutas a áreas
    path('areas/list/', AreaListView.as_view(), name='areas_list'),
    #rutas a maquinas
    path('maquinas/list/', MaquinaListView.as_view(), name='maquinas_list'),
    #rutas a cabezales
    path('cabezales/list/', CabezalListView.as_view(), name='cabezales_list'),
    #rutas a plantas
    path('plantas/list/', PlantaListView.as_view(), name='plantas_list'),
    #rutas a proveedores
    path('proveedores/list/', ProveedorListView.as_view(), name='proveedores_list'),
    #rutas a turnos
    path('turnos/list/', TurnoListView.as_view(), name='turnos_list'),
    #rutas a silos
    path('silos/list/', SiloListView.as_view(), name='silos_list'),
    ]