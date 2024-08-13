from django.urls import path
from .views import ReporteMensual, ReporteRX50, ReporteRX51

app_name = 'reportes'   

urlpatterns = [
    path('reporte-mensual/', ReporteMensual.as_view(), name='reporte_mensual'),
    path('reporte-Rx50/<int:pk>', ReporteRX50.as_view(), name='reporte_Rx50'),
    #reporte rx51
    path('reporte-mensual/', ReporteMensual.as_view(), name='reporte_mensual'),
    path('reporte-Rx51/<int:pk>', ReporteRX51.as_view(), name='reporte_Rx51')
    
    
]
