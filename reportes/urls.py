from django.urls import path
from .views import *

app_name = 'reportes'   

urlpatterns = [
    path('reporte-mensual/', ReporteMensualView.as_view(), name='reporte_mensual'),
    path('reporte-volumen-neto/', VolumenNetoView.as_view(), name='reporte_Volumen_Neto'),
]