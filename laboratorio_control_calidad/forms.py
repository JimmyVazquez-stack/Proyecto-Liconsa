from django import forms 
from .models import producto_terminado
from django import forms 
from django.forms import inlineformset_factory
from .models import *

class TerminadoEncabForm(forms.ModelForm):
    
    class Meta:
        model = terminadoEncab
        exclude = ('estatus',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'id': field, 'name': field})



class TerminadoForm(forms.ModelForm):
    
    class Meta:
        model = producto_terminado
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({'class' : 'form-control'})


class permisosForm(forms.ModelForm):
    
    status = [
    ('True','Permitido edición'),
    ('False','No se puede editar')
    ]
    estatus = forms.ChoiceField(choices=status,widget=forms.RadioSelect)



    class Meta:
        model = producto_terminado
        fields = [
            'id',
            'estatus',
            ]
        
        labels = {
            'id':'id',
            'estatus':'Permisos',
        }

        
TerminadoFormSet = inlineformset_factory(terminadoEncab, producto_terminado, fields='__all__', extra=3, can_delete=False)    
