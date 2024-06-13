from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from .models import Usuario
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView


class LoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('laboratorio_control_calidad:index')



class PerfilView(LoginRequiredMixin, DetailView):
    template_name = 'perfil.html'
    model = Usuario

    def get_object(self):
        return get_object_or_404(Usuario, username=self.request.user.username)