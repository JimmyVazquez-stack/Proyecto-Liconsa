from django.urls import path
from .views import index

name_app = 'mantenimiento'     

urlpatterns = [
    path('', index.as_view(), name='index'),
    
]