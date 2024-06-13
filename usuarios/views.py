from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView
from django.views.generic import ListView
from .models import Usuario


class LoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('laboratorio_control_calidad:index')


class PerfilView(LoginRequiredMixin, ListView):
    template_name = 'perfil.html'
    model = Usuario
    
    def get_queryset(self):
        return Usuario.objects.filter(username=self.request.user)
    
    