from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from .models import Usuario
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, CreateView, ListView, View, UpdateView
from .forms import UserCreationForm, EditarUsuarioForm
from django.contrib import messages
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# Sobrescribir la vista de inicio de sesión para redirigir a la página de inicio
class LoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('laboratorio_control_calidad:index')


#CRUD de usuarios
# Deshabilitar la protección CSRF
@method_decorator(csrf_exempt, name='dispatch')
class CrearUsuarioView(LoginRequiredMixin, CreateView, PermissionRequiredMixin):
    form_class = UserCreationForm
    model = Usuario
    permission_required = 'usuarios.add_usuario'
    template_name = 'crear_usuario.html'
    success_url = reverse_lazy('usuarios:listar_usuarios')
    success_message = 'Usuario creado exitosamente'
    login_url = reverse_lazy('usuarios:login')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        if Usuario.objects.filter(username=username).exists():
            form.add_error('username', 'El nombre de usuario ya existe')
            return self.form_invalid(form)
        else:
            response = super().form_valid(form)
            messages.success(self.request, self.success_message)
            return response
        

class PerfilView(LoginRequiredMixin, DetailView):
    template_name = 'perfil.html'
    model = Usuario
    login_url = reverse_lazy('usuarios:login')

    def get_object(self):
        return get_object_or_404(Usuario, username=self.request.user.username)


class EditarUsuarioView(LoginRequiredMixin, UpdateView, PermissionRequiredMixin):
    modal = Usuario
    form_class = EditarUsuarioForm
    template_name = 'editar_usuario.html'
    success_url = reverse_lazy('usuarios:listar_usuarios')
    
    def get_object(self, queryset=None):
        # Usa 'id' en lugar de 'pk'
        id_ = self.kwargs.get("id")
        return get_object_or_404(Usuario, id=id_)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Asegúrate de usar 'id' en lugar de 'pk' para generar la URL de acción
        context['action'] = reverse_lazy('usuarios:editar_usuario', kwargs={'id': self.object.id})
        return context   


class EliminarUsuarioView(View):
    def delete(self, request, user_id):
        try:
            usuario = Usuario.objects.get(id=user_id)
            usuario.delete()
            return JsonResponse({'message': 'Usuario eliminado exitosamente'})
        except Usuario.DoesNotExist:
            return JsonResponse({'error': 'El usuario no existe'}, status=404)


class ListarUsuariosView(LoginRequiredMixin, ListView, PermissionRequiredMixin):
    model = Usuario
    template_name = 'listar_usuarios.html'
    permission_required = 'usuarios.view_usuario'
    login_url = reverse_lazy('usuarios:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Excluir usuarios staff al contar
        context['total_usuarios'] = self.model.objects.exclude(
            is_staff=True).count()
        context['usuario_autenticado_username'] = self.request.user.username # Obtener el id del usuario autenticado
        return context


class UsuariosDataView(LoginRequiredMixin, View, PermissionRequiredMixin):
    model = Usuario
    login_url = reverse_lazy('usuarios:login')

    def get(self, request, *args, **kwargs):
        # Filtrar para excluir usuarios que son staff
        usuarios_queryset = self.model.objects.filter(
            is_staff=False).select_related('area').prefetch_related('groups')
        usuarios_list = []

        for usuario in usuarios_queryset:
            # Convertir el modelo Usuario a un diccionario
            usuario_dict = model_to_dict(usuario, fields=[
                                         field.name for field in usuario._meta.fields if field.name != 'password'])
            # Personalizar el diccionario para incluir el campo 'grupo'
            usuario_dict['grupo'] = ', '.join(
                [group.name for group in usuario.groups.all()])
            # Añadir el nombre del área al diccionario, asegurándose de que el área existe
            usuario_dict['area'] = usuario.area.nombre if usuario.area else None
            usuarios_list.append(usuario_dict)

        return JsonResponse({'data': usuarios_list}, safe=False)
