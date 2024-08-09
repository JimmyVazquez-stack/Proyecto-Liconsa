# reportes/serializers.py

from rest_framework import serializers
from laboratorio_control_calidad.models import LecheReconsSilos
from laboratorio_control_calidad.models import producto_terminado

class LecheReconsSilosSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecheReconsSilos
        fields = ['fecha_Hora', 'volumen', 'aspecto', 'sabor', 'olor', 'temperatura', 'ph','acidez','densidad','s_g_w_v', 's_n_g_Stsg_wv', 'st_wv', 'proteina', 'encabezado_id', 'producto_id', 'silo_id']  # Incluye todos los campos necesarios
class ProductoTerminadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = producto_terminado
        fields = ['fecha_Hora', 'volumen', 'aspecto', 'sabor', 'olor', 'temperatura', 'ph','acidez','densidad','s_g_w_v', 's_n_g_Stsg_wv', 'st_wv', 'proteina', 'encabezado_id', 'producto_id', 'silo_id']  # Incluye todos los campos necesarios