from django.urls import path
from . import views

app_name = 'reportes'   

urlpatterns = [
    path('reporte-Rx50/<int:pk>', views.ReporteRX50.as_view(), name='reporte_Rx50'),
    #reporte rx51
    path('reporte-Rx51/<int:pk>', views.ReporteRX51.as_view(), name='reporte_Rx51'),
    #URLS para reporte mensual
    path('reporte-mensual-lab/', views.ReporteMensualView.as_view(), name='reporte_mensual'),
    path('reporte-mensual-lab/pdf/', views.PDFGeneratorView.as_view(), name='reporte_mensual_pdf'),
    path('api/composicion_fisicoquimica/', views.ComposicionFisicoquimicaDataView.as_view(), name='composicion_fisioquimica_api'),
    path('api/tipos_productos/', views.TipoPorductoDataView.as_view(), name='tipos_productos_api'),
]
