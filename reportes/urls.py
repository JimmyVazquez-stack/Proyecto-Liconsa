from django.urls import path
from . import views


app_name = 'reportes'   

urlpatterns = [
    path('reporte-Rx50/<int:pk>', views.ReporteRX50.as_view(), name='reporte_Rx50'),
    path('reporte-Rx51/<int:pk>', views.ReporteRX51.as_view(), name='reporte_Rx51'),

    #URLS para reporte R49 JuanCarlosM
    path('reporte-volumen-neto/', views.VolumenNetoView.as_view(), name='reporte_Volumen_Neto'),
    path('densidad-Ponderada-Data/', views.CalculosR49DataView.as_view(), name='densidad_Ponderada_Data'), #calculos para tabla peso neto
    path('diario-Semanal-Data/', views.ReporteR49RangoFechaView.as_view(), name='diario_Semanal_Data'), #no se muestran los datos directo en la url, pero si desde el modal con rango de fecha
    path('reporte-Diario/<int:id>', views.MostrarDiarioView.as_view(), name='reporte_Diario'), #Para reporte diario por maquinas, peso neto
    #URLS para reporte mensual
    path('reporte-mensual-lab/', views.ReporteMensualView.as_view(), name='reporte_mensual'),
    path('reporte-mensual-lab/pdf/', views.PDFGeneratorView.as_view(), name='reporte_mensual_pdf'),
    path('api/composicion_fisicoquimica/', views.ComposicionFisicoquimicaDataView.as_view(), name='composicion_fisioquimica_api'),

]