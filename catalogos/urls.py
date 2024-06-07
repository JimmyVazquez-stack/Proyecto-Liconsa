from django.urls import path
from .views import LecheriaListView, AñadirLecheriaView, LecheriaDataView, ActualizarLecheriaView

app_name = 'catalogos'

urlpatterns = [
    path('lecherias/list/', LecheriaListView.as_view(), name='lecherias_list'),
    path('añadir_lecheria/', AñadirLecheriaView.as_view(), name='añadir_lecheria'),
    path('lecherias/list/data/', LecheriaDataView.as_view(), name='lecherias_data'),
    path('actualizar_lecheria/', ActualizarLecheriaView.as_view(), name='actualizar_lecheria'),
    ]