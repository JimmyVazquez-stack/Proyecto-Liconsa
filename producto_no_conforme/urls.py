from django.urls import path
from .views import *

app_name = 'producto_no_conforme'

urlpatterns = [
    path('lecherias/', LecheriaListView.as_view(), name='lecherias'),
    path('lecherias/data/', LecheriaRotosDataView.as_view(), name='lecherias_data'),
    path('lecherias/muestreo_rotos/', CrearMuestreoRotos.as_view(), name='muestreo_rotos'),
    
# Mal sellados -------------------------------------
    path('ms_encabView', malSelladosEncabView.as_view(), name='ms_encabView'),
    path('ms_encabUpdate/<int:pk>', malSelladosUpdate.as_view(), name='ms_encabUpdate'),
    path('ms_delete/<int:pk>', MalSelladosDelete.as_view(), name='ms_delete'), 
    
]