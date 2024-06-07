from django.urls import path
from .views import LecheriaListView, LecheriaDataView, CrearMuestreoRotos

app_name = 'producto_no_conforme'

urlpatterns = [
    path('lecherias/', LecheriaListView.as_view(), name='lecherias'),
    path('lecherias/data/', LecheriaDataView.as_view(), name='lecherias_data'),
    path('lecherias/muestreo_rotos/', CrearMuestreoRotos.as_view(), name='muestreo_rotos'),
]