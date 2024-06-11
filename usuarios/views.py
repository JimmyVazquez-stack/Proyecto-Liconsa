from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import TemplateView


class index(LoginRequiredMixin, TemplateView):
    template_name = 'iniciar_sesion.html'
    login_url = reverse_lazy('laboratorio_control_calidad:index') 
    