from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from .models import Usuario
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, CreateView, ListView
from .forms import UserCreationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import JsonResponse

class LoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('laboratorio_control_calidad:index')



class PerfilView(LoginRequiredMixin, DetailView):
    template_name = 'perfil.html'
    model = Usuario
    login_url = reverse_lazy('usuarios:login')
    
    def get_object(self):
        return get_object_or_404(Usuario, username=self.request.user.username)
    
    
class CrearUsuarioView(LoginRequiredMixin,CreateView, PermissionRequiredMixin):
    form_class = UserCreationForm
    model = Usuario
    permission_required = 'usuarios.add_usuario'
    template_name = 'crear_usuario.html'
    success_url = reverse_lazy('usuarios:crear_usuario')
    success_message = 'Usuario creado exitosamente'
    login_url  = reverse_lazy('usuarios:login')
    
    def form_valid(self, form):
        username = form.cleaned_data['username']
        if Usuario.objects.filter(username=username).exists():
            form.add_error('username', 'El nombre de usuario ya existe')
            return self.form_invalid(form)
        else:
            response = super().form_valid(form)
            messages.success(self.request, self.success_message)
            return response


class ListarUsuariosView(LoginRequiredMixin,ListView, PermissionRequiredMixin):
    model = Usuario
    template_name = 'listar_usuarios.html'
    permission_required = 'usuarios.view_usuario'
    login_url = reverse_lazy('usuarios:login')
    
    def render_to_response(self, context, **response_kwargs):
        # Verificar si la solicitud es AJAX
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            data = list(self.model.objects.values('id', 'nombre', 'email'))  # Asegúrate de ajustar los campos según tu modelo
            return JsonResponse({'data': data})
        else:
            return super().render_to_response(context, **response_kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_usuarios'] = self.model.objects.count()
        return context