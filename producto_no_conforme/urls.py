from django.urls import path
from producto_no_conforme.views import * 

urlpatterns = [
    # path('', views.home, name='home'),
    
    path('',Producto_no_Conforme_Home.as_view(), name='home_producto_no_conforme'),
    path('Registrar/',Producto_no_Conforme_Registro.as_view(), name='registro_producto_no_conforme'),
    
]