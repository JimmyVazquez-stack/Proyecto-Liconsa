from django.urls import path
from .views import LecheriaListView, LecheriaRotosDataView, CrearMuestreoRotos

app_name = 'producto_no_conforme'

urlpatterns = [
    path('lecherias/', LecheriaListView.as_view(), name='lecherias'),
    path('lecherias/data/', LecheriaRotosDataView.as_view(), name='lecherias_data'),
    path('lecherias/muestreo_rotos/', CrearMuestreoRotos.as_view(), name='muestreo_rotos'),
]