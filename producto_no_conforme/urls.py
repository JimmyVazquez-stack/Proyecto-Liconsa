from django.urls import path
from . import views

app_name = 'producto_no_conforme'

urlpatterns = [
    path('lecherias/', views.LecheriaListView.as_view(), name='lecherias'),
    path('lecherias/data/', views.LecheriaRotosDataView.as_view(), name='lecherias_data'),
    path('lecherias/muestreo_rotos/', views.CrearMuestreoRotos.as_view(), name='muestreo_rotos'),
]