from django.urls import path
from . import views

app_name = 'mantenimiento'     

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('agua_alimentacion_proceso/', views.agua_alimentacion_proceso.as_view(), name='agua_alimentacion_proceso'),
    
]