from django import forms 
from .models import producto_terminado

class TerminadoForm(forms.ModelForm):
    class Meta:
        model = producto_terminado
        fields ='__all__'
        
        fields = [
            'lotCad',
            'planta',
            'turno',
            'silo',
            'maquina',
            'hora',
            'producto',
            'volumen',
            'aspecto',
            'sabor',
            'olor',
            'temperatura',
            'acidez',
            'densidad',
            'sg',
            'sng',
            'st',
            'proteina'
        ] 
        
        labels = {
            'lotCad':'Lote de caducidad',
            'planta':'Planta',
            'turno': 'Turno',
            'silo': 'No. de silo',
            'maquina': 'Maquina',
            'hora': 'Hora',
            'producto': 'Producto',
            'volumen': 'Volumen(L)',
            'aspecto': 'Aspecto',
            'sabor':'Sabor',
            'olor':'Olor',
            'temperatura' :'Temperatura(°C)',
            'acidez':'Ácidez g/l',
            'densidad':'Densidad g/ml',
            'sg':'S.G g/l',
            'sng':'S.N.G g/l',
            'st':'S.T g/l',
            'proteina':'Proteina g/l'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['lotCad'].widget.attrs.update({'class': 'form-control'})
        self.fields['planta'].widget.attrs.update({'class': 'form-control'})
        self.fields['turno'].widget.attrs.update({'class': 'form-control'})
        self.fields['silo'].widget.attrs.update({'class': 'form-control'})
        self.fields['maquina'].widget.attrs.update({'class': 'form-control'})
        self.fields['hora'].widget.attrs.update({'class': 'form-control'})
        self.fields['producto'].widget.attrs.update({'class': 'form-control'})
        self.fields['volumen'].widget.attrs.update({'class': 'form-control'})
        self.fields['aspecto'].widget.attrs.update({'class': 'form-control'})
        self.fields['sabor'].widget.attrs.update({'class': 'form-control'})
        self.fields['olor'].widget.attrs.update({'class': 'form-control'})
        self.fields['temperatura'].widget.attrs.update({'class': 'form-control'})
        self.fields['acidez'].widget.attrs.update({'class': 'form-control'})
        self.fields['densidad'].widget.attrs.update({'class': 'form-control'})
        self.fields['sg'].widget.attrs.update({'class': 'form-control'})
        self.fields['sng'].widget.attrs.update({'class': 'form-control'})
        self.fields['st'].widget.attrs.update({'class': 'form-control'})
        self.fields['proteina'].widget.attrs.update({'class': 'form-control'})


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

    
