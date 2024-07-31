from django.urls import path
from .views import (
    LecheriaListView, 
    LecheriaDataView, 
    PoblacionListView, 
    AreaListView, 
    MaquinaListView, 
    MaquinaDataView,
    CabezalListView, 
    PlantaListView, 
    ProveedorListView,
    SiloListView,
    TurnoListView,
    DataPoblacionView,
    PlantaDataView,
    TurnoDataView,
    DataSilosView,
    DataAreaView,
    CabezalDataView,
    ProductoDataView,
    ProductoListView,
    TipoProductoDataView,
    TipoProductoListView,
    ProveedorDataView,
    RutaListView,
    RutaDataView,
    RutaCreateView,
    RutaUpdateView,
    RutaDeleteView,
    AreaCreateView,
    AreaUpdateView,
    AreaDeleteView,
    MaquinaCreateView,
    MaquinaUpdateView,
    MaquinaDeleteView,
    PlantaCreateView,
    PlantaUpdateView,
    PlantaDeleteView
    )

app_name = 'catalogos'

urlpatterns = [
    path('lecherias/list/', LecheriaListView.as_view(), name='lecherias_list'),
    path('lecherias/list/data/', LecheriaDataView.as_view(), name='lecherias_data'),
    #rutas a poblaciones
    path('poblaciones/list/', PoblacionListView.as_view(), name='poblaciones_list'),
    path('poblaciones/list/data/', DataPoblacionView.as_view(), name='poblaciones_data'),
    #rutas a áreas
    path('areas/list/', AreaListView.as_view(), name='areas_list'),
    path('areas/list/data/', DataAreaView.as_view(), name='areas_data'),
    path('areas/create/', AreaCreateView.as_view(), name='crear_area'),
    path('areas/update/<int:pk>/', AreaUpdateView.as_view(), name='actualizar_area'),
    path('areas/delete/<int:id>/', AreaDeleteView.as_view(), name='eliminar_area'),
    #rutas a maquinas
    path('maquinas/list/', MaquinaListView.as_view(), name='maquinas_list'),
    path('maquinas/list/data/', MaquinaDataView.as_view(), name='maquinas_data'),
    path('maquinas/create/', MaquinaCreateView.as_view(), name='crear_maquina'),
    path('maquinas/update/<int:pk>/', MaquinaUpdateView.as_view(), name='actualizar_maquina'),
    path('maquinas/delete/<int:id>/', MaquinaDeleteView.as_view(), name='eliminar_maquina'),
    #rutas a cabezales
    path('cabezales/list/', CabezalListView.as_view(), name='cabezales_list'),
    path('cabezales/list/data/', CabezalDataView.as_view(), name='cabezales_data'),
    #rutas a plantas
    path('plantas/list/', PlantaListView.as_view(), name='plantas_list'),
    path('plantas/list/data/', PlantaDataView.as_view(), name='plantas_data'),
    path('plantas/create/', PlantaCreateView.as_view(), name='crear_planta'),
    path('plantas/update/<int:pk>/', PlantaUpdateView.as_view(), name='actualizar_planta'),
    path('plantas/delete/<int:pk>/', PlantaDeleteView.as_view(), name='eliminar_planta'),
    #rutas a proveedores
    path('proveedores/list/', ProveedorListView.as_view(), name='proveedores_list'),
    path('proveedores/list/data/', ProveedorDataView.as_view(), name='proveedores_data'),
    #rutas a turnos
    path('turnos/list/', TurnoListView.as_view(), name='turnos_list'),
    path('turnos/list/data/', TurnoDataView.as_view(), name='turnos_data'),
    #rutas a silos
    path('silos/list/', SiloListView.as_view(), name='silos_list'),
    path('silos/list/data/', DataSilosView.as_view(), name='silos_data'),
    #rutas a gestion de productos
    path('productos/list/', ProductoListView.as_view(), name='productos_list'),
    path('productos/list/data/', ProductoDataView.as_view(), name='productos_data'),
    path('tipo_producto/list/', TipoProductoListView.as_view(), name='tipo_producto_list'),
    path('tipo_producto/list/data/', TipoProductoDataView.as_view(), name='tipo_producto_data'),
    #rutas
    path('rutas/list/', RutaListView.as_view(), name='rutas_list'),
    path('rutas/list/data/', RutaDataView.as_view(), name='rutas_data'),
    path('rutas/create/', RutaCreateView.as_view(), name='rutas_create'),
    path('rutas/update/<int:pk>/', RutaUpdateView.as_view(), name='rutas_update'),
    path('rutas/delete/<int:id>/', RutaDeleteView.as_view(), name='rutas_delete'),
    ]