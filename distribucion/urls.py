from django.urls import path
from distribucion import views  

app_name = 'distribucion'

urlpatterns = [
    # path('distribucion/', views.index.as_view(), name='index'),
  
   #[Inicio] rutas para el CRUD de Orden Despacho PNC- ------------------------------------------------------]
    path('encabOrdenDesp_List/', views.EncabOrdenDespListView.as_view(), name='encabOrdenDesp_List'),
    path('encabOrdenDesp_Delete/<int:pk>/', views.EncabOrdenDespDeleteView.as_view(), name='encabOrdenDesp_Delete'),
    path('encabOrdenDesp_Update/<int:pk>/', views.EncabOrdenDespUpdateView.as_view(), name='encabOrdenDesp_Update'),

    path('ordenDesp_Create/', views.OrdenDespCreateView.as_view(), name='ordenDesp_Create'),
    path('ordenDesp_List/', views.OrdenDespListView.as_view(), name='ordenDesp_List'),
    path('ordenDesp_Delete/<int:pk>', views.OrdenDespDeleteView.as_view(), name='ordenDesp_Delete'),
    path('ordenDesp_Update/<int:pk>', views.OrdenDespUpdateView.as_view(), name='ordenDesp_Update'),
    #[Fin] rutas para el CRUD orden despacho PNC--------------------------------------------------------------]
]