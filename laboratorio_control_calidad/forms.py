from django import forms 
from .models import TablaR49 

class TablaR49Form(forms.ModelForm): 
    class Meta: 
        model = TablaR49 
        fields = ['num_maquina', 'num_datos', 'promedio','desv_std','maximo','minimo'] 