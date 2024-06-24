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
from django.contrib.auth.forms import UserCreationForm


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
    
    def get(self, request):
        form = self.form_class()
        return render(request, 'crear_usuario.html', {'form': form})
    