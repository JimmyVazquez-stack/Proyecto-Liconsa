from django.urls import path
from .views import LecheriaListView, LecheriaDataView

app_name = 'producto_no_conforme'

urlpatterns = [
    path('lecherias/', LecheriaListView.as_view(), name='lecherias'),
    path('lecherias/data/', LecheriaDataView.as_view(), name='lecherias_data'),
]