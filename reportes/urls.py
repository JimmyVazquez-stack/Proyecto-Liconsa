from django.urls import path
from reportes.views import CalculosR49DataView, VolumenNetoView, ReporteMensualView

app_name = 'reportes'   

urlpatterns = [
    path('reporte-mensual/', ReporteMensualView.as_view(), name='reporte_mensual'),
    path('reporte-volumen-neto/', VolumenNetoView.as_view(), name='reporte_Volumen_Neto'),
    path('densidad-Ponderada-Data/', CalculosR49DataView.as_view(), name='densidad_Ponderada_Data'),
]