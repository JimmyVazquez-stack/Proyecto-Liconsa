from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from .models import Usuario
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView, CreateView
from .forms import UserCreationForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages


class LoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('laboratorio_control_calidad:index')



class PerfilView(LoginRequiredMixin, DetailView):
    template_name = 'perfil.html'
    model = Usuario

    def get_object(self):
        return get_object_or_404(Usuario, username=self.request.user.username)
    
    
class CrearUsuarioView(CreateView, PermissionRequiredMixin):
    form_class = UserCreationForm
    model = Usuario
    permission_required = 'usuarios.add_usuario'
    template_name = 'crear_usuario.html'
    success_url = reverse_lazy('usuarios:crear_usuario')
    success_message = 'Usuario creado exitosamente'
    
    def form_valid(self, form):
        username = form.cleaned_data['username']
        if Usuario.objects.filter(username=username).exists():
            form.add_error('username', 'El nombre de usuario ya existe')
            return self.form_invalid(form)
        else:
            response = super().form_valid(form)
            messages.success(self.request, self.success_message)
            return response
