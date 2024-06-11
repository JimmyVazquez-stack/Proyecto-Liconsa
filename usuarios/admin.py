from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User, Group
from .forms import UserChangeForm, UserCreationForm
'''
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    def get_grupo(self, obj):
        groups = obj.groups.all()
        if groups:
            return ", ".join([group.name for group in groups])
        return '-'
    get_grupo.short_description = 'Grupo'

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_grupo')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'grupo', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'grupo')}
        ),
    )

    def save_model(self, request, obj, form, change):
        obj.save()
        if 'grupo' in form.cleaned_data:
            grupo = form.cleaned_data['grupo']
            if grupo:
                obj.groups.set([grupo])
                obj.user_permissions.set(grupo.permissions.all())
            else:
                obj.groups.clear()
                obj.user_permissions.clear()
        else:
            obj.groups.clear()
            obj.user_permissions.clear()

#Registrar los modelos en el admin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
'''

'''
En este archivo se define la configuración del admin de Django para los modelos de usuarios y grupos.
'''