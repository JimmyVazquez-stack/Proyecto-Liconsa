from django.urls import path
from .views import ReporteMensualView, ReporteRX51

app_name = 'reportes'   

urlpatterns = [
    path('reporte-mensual/', ReporteMensualView.as_view(), name='reporte_mensual'),
    path('reporte-Rx51/<int:pk>', ReporteRX51.as_view(), name='reporte_Rx51')
]