from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Area


class UsuarioAdmin(UserAdmin):
    model = Usuario
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Información personal', {'fields': ('first_name', 'last_name', 'email', 'area', 'telefono')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
        ('Fechas importantes', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'area', 'telefono', 'is_active', 'is_staff', 'is_superuser', 'groups'),
        }),
    )
    list_display = ('username', 'first_name', 'last_name', 'email', 'telefono', 'is_staff', 'area', 'get_groups')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'area', 'telefono')
    ordering = ('username',)
    
    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])
    get_groups.short_description = 'Grupos'
    
admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Area)
