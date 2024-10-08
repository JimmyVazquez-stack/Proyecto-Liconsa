from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'usuarios'

urlpatterns = [
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('perfil/', views.PerfilView.as_view(), name='perfil'),
    path('crear_usuario/', views.CrearUsuarioView.as_view(), name='crear_usuario'),
    path('listar_usuarios/', views.ListarUsuariosView.as_view(), name='listar_usuarios'),
    path('data/', views.UsuariosDataView.as_view(), name='usuarios_data'),
    path('eliminar_usuario/<int:user_id>/', views.EliminarUsuarioView.as_view(), name='eliminar_usuario'),
    path('editar_usuario/<int:id>/', views.EditarUsuarioView.as_view(), name='editar_usuario'),
]