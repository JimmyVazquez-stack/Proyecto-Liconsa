from django.urls import path
from .views import PDFGeneratorView

app_name = 'reportes'   

urlpatterns = [
    path('reporte-mensual/', PDFGeneratorView.as_view(), name='reporte_mensual')
]