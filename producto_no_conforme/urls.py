from django.urls import path
from .views import   render_pdf_view, LecheriaListView, LecheriaRotosDataView, CrearMuestreoRotos, VerReporteView

app_name = 'producto_no_conforme'

urlpatterns = [
    path('lecherias/', LecheriaListView.as_view(), name='lecherias'),
    path('lecherias/data/', LecheriaRotosDataView.as_view(), name='lecherias_data'),
    path('lecherias/muestreo_rotos/', CrearMuestreoRotos.as_view(), name='muestreo_rotos'),
    path('ver-reporte/', VerReporteView.as_view(), name='ver_reporte'),
    path('ver-reporte-pdf/', render_pdf_view, name='ver_reporte_pdf')
]