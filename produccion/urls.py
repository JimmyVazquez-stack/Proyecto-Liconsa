from django.urls import path
from .views import index

name_app = 'produccion' 

urlpatterns = [
    path('', index.as_view(), name='index'),
    
]