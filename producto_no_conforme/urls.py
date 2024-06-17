from django.urls import path
from .views import LecheriaListView, LecheriaRotosDataView, CrearMuestreoRotos

app_name = 'producto_no_conforme'

urlpatterns = [
<<<<<<< HEAD
    

=======
>>>>>>> d2087161ed664a5d99d597d283d3efa8089d7dc6
    path('lecherias/', LecheriaListView.as_view(), name='lecherias'),
    path('lecherias/data/', LecheriaRotosDataView.as_view(), name='lecherias_data'),
    path('lecherias/muestreo_rotos/', CrearMuestreoRotos.as_view(), name='muestreo_rotos'),
]