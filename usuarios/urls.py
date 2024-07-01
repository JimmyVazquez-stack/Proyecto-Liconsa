from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import LoginView

app_name = 'usuarios'

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path ('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('perfil/', views.PerfilView.as_view(), name='perfil'),
    path('crear_usuario/', views.CrearUsuarioView.as_view(), name='crear_usuario'),
    path('listar_usuarios/', views.ListarUsuariosView.as_view(), name='listar_usuarios'),
    path('data/', views.UsuariosDataView.as_view(), name='usuarios_data'),
]