from django import forms 
from .models import TablaR49, Densidadpt, Pesoenvvacio, Pesobruto #Pesoneto



class TablaR49Form(forms.ModelForm):
    class Meta:
        model = TablaR49
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

