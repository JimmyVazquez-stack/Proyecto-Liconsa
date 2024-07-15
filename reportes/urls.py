from django.urls import path
from .views import PDFGeneratorView
from .views import ReporteRX50

app_name = 'reportes'   

urlpatterns = [
    path('reporte-mensual/', PDFGeneratorView.as_view(), name='reporte_mensual'),
    path('reporte-Rx50/<int:pk>', ReporteRX50.as_view(), name='reporte_Rx50'),
]