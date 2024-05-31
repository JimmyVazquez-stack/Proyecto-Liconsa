from django.urls import path
from .views import index

name_app = 'laboratorio_control_calidad'

urlpatterns = [
    path('', index.as_view(), name='index'),

]
