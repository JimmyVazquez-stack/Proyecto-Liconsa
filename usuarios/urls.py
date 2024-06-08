from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [

    path('login/', auth_views.LoginView.as_view(template_name='usuarios/login.html'), name='login'),
    ]
