# serializers.py
from rest_framework import serializers
from .models import CalidadMicrobiologicaEncabezado, CalidadMicrobiologica
from catalogos.models import Planta, Producto

class CalidadMicrobiologicaEncabezadoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CalidadMicrobiologicaEncabezado
        fields = ['id', 'folio', 'fecha_creacion']

class PlantaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planta
        fields = ['id', 'nombre']

class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = ['id', 'nombre']


class CalidadMicrobiologicaSerializer(serializers.ModelSerializer):
    planta = PlantaSerializer(read_only=True)
    producto = ProductoSerializer(read_only=True)
    edit_url = serializers.SerializerMethodField()
    delete_url = serializers.SerializerMethodField()

    class Meta:
        model = CalidadMicrobiologica
        fields = ['id', 'fechaHora', 'planta', 'producto', 'organismos_coliformes', 'edit_url', 'delete_url']

    def get_edit_url(self, obj):
        return f'/control_calidad/calidad_microbiologica/edit/{obj.id}/'

    def get_delete_url(self, obj):
        return f'/control_calidad/calidad_microbiologica/delete/{obj.id}/'