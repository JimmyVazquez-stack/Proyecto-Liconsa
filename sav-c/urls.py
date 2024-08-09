"""
URL configuration for siscoca project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', auth_views.LoginView.as_view(), name='login'),
    path('usuarios/', include('usuarios.urls')),
    path('control_calidad/', include('laboratorio_control_calidad.urls')),
    path('almacen/', include('almacen.urls')),
    path('produccion/', include('produccion.urls')),
    path('mantenimiento/', include('mantenimiento.urls')),
    path('producto_no_conforme/', include('producto_no_conforme.urls')),
    path('catalogos/', include('catalogos.urls')),
    path('reportes/', include('reportes.urls', namespace='reportes')),
    path('api/', include('reportes.urls', namespace='api')),
    path('admin/', admin.site.urls),
]
