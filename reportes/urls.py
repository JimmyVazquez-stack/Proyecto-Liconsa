from django.urls import path
from . import views
app_name = 'reportes'   

urlpatterns = [
    path('reporte-Rx50/<int:pk>', views.ReporteRX50.as_view(), name='reporte_Rx50'),
    path('reporte-Rx51/<int:pk>', views.ReporteRX51.as_view(), name='reporte_Rx51'),

    #URLS para reporte mensual
    path('reporte-mensual-lab/', views.ReporteMensual.as_view(), name='reporte_mensual'),
    path('reporte-mensual-lab/pdf/', views.PDFGeneratorView.as_view(), name='reporte_mensual_pdf'),

]