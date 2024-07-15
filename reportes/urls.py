from django.urls import path
from .views import PDFGeneratorView
from .views import ReporteRX50, ReporteRX51

app_name = 'reportes'   

urlpatterns = [
    path('reporte-mensual/', PDFGeneratorView.as_view(), name='reporte_mensual'),
    path('reporte-Rx50/<int:pk>', ReporteRX50.as_view(), name='reporte_Rx50'),
    path('reporte-Rx51/<int:pk>', ReporteRX51.as_view(), name='reporte_Rx51')
]