from django.urls import path
from .views import (index,
                    agua_alimentacion_proceso,) 

app_name = 'mantenimiento'     

urlpatterns = [
    path('', index.as_view(), name='index'),
    path('agua_alimentacion_proceso/', agua_alimentacion_proceso.as_view(), name='agua_alimentacion_proceso'),
    
]