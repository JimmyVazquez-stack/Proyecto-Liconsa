from django.urls import path
from . import views

app_name = 'catalogos'

urlpatterns = [
    path('lecherias/list/', views.LecheriaListView.as_view(), name='lecherias_list'),
    path('lecherias/list/data/', views.LecheriaDataView.as_view(), name='lecherias_data'),
    path('lecherias/create/', views.LecheriaCreateView.as_view(), name='crear_lecheria'),
    path('lecherias/update/<int:pk>/', views.LecheriaUpdateView.as_view(), name='actualizar_lecheria'),
    path('lecherias/delete/<int:pk>/', views.LecheriaDeleteView.as_view(), name='eliminar_lecheria'),
    #rutas a poblaciones
    path('poblaciones/list/', views.PoblacionListView.as_view(), name='poblaciones_list'),
    path('poblaciones/list/data/', views.DataPoblacionView.as_view(), name='poblaciones_data'),
    path('poblaciones/create/', views.PoblacionCreateView.as_view(), name='crear_poblacion'),
    path('poblaciones/update/<int:pk>/', views.PoblacionUpdateView.as_view(), name='actualizar_poblacion'),
    path('poblaciones/delete/<int:pk>/', views.PoblacionDeleteView.as_view(), name='eliminar_poblacion'),
    #rutas a áreas
    path('areas/list/', views.AreaListView.as_view(), name='areas_list'),
    path('areas/list/data/', views.DataAreaView.as_view(), name='areas_data'),
    path('areas/create/', views.AreaCreateView.as_view(), name='crear_area'),
    path('areas/update/<int:pk>/', views.AreaUpdateView.as_view(), name='actualizar_area'),
    path('areas/delete/<int:pk>/', views.AreaDeleteView.as_view(), name='eliminar_area'),
    #rutas a maquinas
    path('maquinas/list/', views.MaquinaListView.as_view(), name='maquinas_list'),
    path('maquinas/list/data/', views.MaquinaDataView.as_view(), name='maquinas_data'),
    path('maquinas/create/', views.MaquinaCreateView.as_view(), name='crear_maquina'),
    path('maquinas/update/<int:pk>/', views.MaquinaUpdateView.as_view(), name='actualizar_maquina'),
    path('maquinas/delete/<int:id>/', views.MaquinaDeleteView.as_view(), name='eliminar_maquina'),
    #rutas a cabezales
    path('cabezales/list/', views.CabezalListView.as_view(), name='cabezales_list'),
    path('cabezales/list/data/', views.CabezalDataView.as_view(), name='cabezales_data'),
    #rutas a plantas
    path('plantas/list/', views.PlantaListView.as_view(), name='plantas_list'),
    path('plantas/list/data/', views.PlantaDataView.as_view(), name='plantas_data'),
    path('plantas/create/', views.PlantaCreateView.as_view(), name='crear_planta'),
    path('plantas/update/<int:pk>/', views.PlantaUpdateView.as_view(), name='actualizar_planta'),
    path('plantas/delete/<int:pk>/', views.PlantaDeleteView.as_view(), name='eliminar_planta'),
    #rutas a proveedores
    path('proveedores/list/', views.ProveedorListView.as_view(), name='proveedores_list'),
    path('proveedores/list/data/', views.ProveedorDataView.as_view(), name='proveedores_data'),
    path('proveedores/create/', views.ProveedorCreateView.as_view(), name='proveedores_create'),
    path('proveedores/update/<int:pk>/', views.ProveedorUpdateView.as_view(), name='proveedores_update'),
    path('proveedores/delete/<int:pk>/', views.ProveedorDeleteView.as_view(), name='proveedores_delete'),
    #rutas a turnos
    path('turnos/list/', views.TurnoListView.as_view(), name='turnos_list'),
    path('turnos/list/data/', views.TurnoDataView.as_view(), name='turnos_data'),
    path('turnos/create/', views.TurnoCreateView.as_view(), name='turnos_create'),
    path('turnos/update/<int:pk>/', views.TurnoUpdateView.as_view(), name='turnos_update'),
    path('turnos/delete/<int:pk>/', views.TurnoDeleteView.as_view(), name='turnos_delete'),
    #rutas a silos
    path('silos/list/', views.SiloListView.as_view(), name='silos_list'),
    path('silos/list/data/', views.DataSilosView.as_view(), name='silos_data'),
    #rutas a gestion de productos
    path('productos/list/', views.ProductoListView.as_view(), name='productos_list'),
    path('productos/list/data/', views.ProductoDataView.as_view(), name='productos_data'),
    path('productos/create/', views.ProductoCreateView.as_view(), name='producto_create'),
    path('productos/update/<int:producto_id>/', views.ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/delete/<int:producto_id>/', views.ProductoDeleteView.as_view(), name='producto_delete'),  
    #rutas a gestion de tipos de productos
    path('tipo_producto/list/', views.TipoProductoListView.as_view(), name='tipo_producto_list'),
    path('tipo_producto/list/data/', views.TipoProductoDataView.as_view(), name='tipo_producto_data'),
    path('tipo_producto/create/', views.TipoProductoCreateView.as_view(), name='tipo_producto_create'),
    #rutas
    path('rutas/list/', views.RutaListView.as_view(), name='rutas_list'),
    path('rutas/list/data/', views.RutaDataView.as_view(), name='rutas_data'),
    path('rutas/create/', views.RutaCreateView.as_view(), name='rutas_create'),
    path('rutas/update/<int:pk>/', views.RutaUpdateView.as_view(), name='rutas_update'),
    path('rutas/delete/<int:id>/', views.RutaDeleteView.as_view(), name='rutas_delete'),
    ]