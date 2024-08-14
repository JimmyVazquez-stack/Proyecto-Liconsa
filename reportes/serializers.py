from rest_framework import serializers
from laboratorio_control_calidad.models import LecheReconsSilos
from laboratorio_control_calidad.models import producto_terminado

class LecheReconsSilosSerializer(serializers.ModelSerializer):
    class Meta:
        model = LecheReconsSilos
        fields = ['fecha_Hora', 'volumen', 'temperatura', 'densidad', 's_g_w_v', 's_n_g_Stsg_wv', 'st_wv','ph', 'producto_id', 'silo_id']  # Incluye todos los campos necesarios
class ProductoTerminadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = producto_terminado
        fields = ['fecha_Hora', 'volumen', 'temperatura', 'ph','acidez','densidad','s_g_w_v', 's_n_g_Stsg_wv', 'st_wv', 'proteina', 'producto_id', 'silo_id']  # Incluye todos los campos necesarios