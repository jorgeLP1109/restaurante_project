
from django.contrib import admin
from django.urls import path, include
from restaurante_app.views import inicio
from restaurante_app import views 
from django.contrib.auth.views import LogoutView
from restaurante_app.views import profile

app_name = 'restaurante_app'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),    
    path('', views.inicio, name='inicio'),
    path('agregar_producto/', views.agregar_producto, name='agregar_producto'),
    path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('cerrar_sesion/', LogoutView.as_view(), name='cerrar_sesion'),
    path('accounts/profile/', profile, name='profile'),
    path('perfil/', views.ver_perfil, name='ver_perfil'),
    path('lista_productos/', views.lista_productos, name='lista_productos'),
    path('editar_producto/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('eliminar_producto/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),
    
    
]
