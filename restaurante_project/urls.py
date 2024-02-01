"""
URL configuration for restaurante_project project.

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
from restaurante_app.views import inicio
from restaurante_app import views 
from django.contrib.auth.views import LogoutView



urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),    
    path('', views.inicio, name='inicio'),
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),
    path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('cerrar_sesion/', LogoutView.as_view(), name='cerrar_sesion'),
    
    
]
