from django import forms 
from .models import *
from django.forms import inlineformset_factory

class EncabTablaR49Form(forms.ModelForm):
    class Meta:
        model = EncabTablaR49
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class' : 'form-control'})

class DensidadptForm(forms.ModelForm):
    class Meta:
        model = Densidadpt
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class' : 'form-control'})

class PesoenvvacioForm(forms.ModelForm):
    class Meta:
        model = Pesoenvvacio
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class' : 'form-control'})

class PesobrutoForm(forms.ModelForm):
    class Meta:
        model = Pesobruto
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class' : 'form-control'})

#FORMSET PAR LA TABLA R49 START
DensidadptFormSet = inlineformset_factory(EncabTablaR49, Densidadpt, fields='__all__', extra=7, can_delete=False)
PesoenvvacioFormSet = inlineformset_factory(EncabTablaR49, Pesoenvvacio, fields='__all__', extra=10, can_delete=False)
PesobrutoFormSet = inlineformset_factory(EncabTablaR49, Pesobruto, fields=['id','fechaHora','cabezal','maquina','planta','producto','valor'], extra=10, can_delete=False)

#FORMSET PAR LA TABLA R49 END

