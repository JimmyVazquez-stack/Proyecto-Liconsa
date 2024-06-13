from django.urls import path
from .views import ReporteMensualView

app_name = 'reportes'   

urlpatterns = [
    path('reporte-mensual/', ReporteMensualView.as_view(), name='reporte_mensual')
]