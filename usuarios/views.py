from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView




class LoginView(LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('laboratorio_control_calidad:index')