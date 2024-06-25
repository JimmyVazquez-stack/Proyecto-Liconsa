from django import forms
from django.contrib.auth.models import User, Group
from .models import Usuario
from catalogos.models import Area

class UserChangeForm(forms.ModelForm):
    grupo = forms.ModelChoiceField(queryset=Group.objects.all(), required=False, label='Grupo')

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser', 'grupo', 'area']

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            # Si la instancia ya existe, se asigna el grupo al que pertenece el usuario
            self.fields['grupo'].initial = self.instance.groups.first()

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            if self.cleaned_data['grupo']:
                user.groups.set([self.cleaned_data['grupo']])
            else:
                user.groups.clear()
        return user


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirma la contraseña', widget=forms.PasswordInput)
    grupo = forms.ModelChoiceField(queryset=Group.objects.all(), required=False, label='Grupo')
    first_name = forms.CharField(label='Nombre(s)', max_length=30, required=False)
    last_name = forms.CharField(label='Apellido', max_length=30, required=False)
    email = forms.EmailField(label='Correo', required=False)
    area = forms.ModelChoiceField(queryset=Area.objects.all(), required=False, label='Área')

    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'grupo', 'area']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            if self.cleaned_data['grupo']:
                user.groups.set([self.cleaned_data['grupo']])
            else:
                user.groups.clear()
        return user

'''
En este archivo se definen los formularios que se utilizarán para la creación y modificación de usuarios en el sistema.
'''
