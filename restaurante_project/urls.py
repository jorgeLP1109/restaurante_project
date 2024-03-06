
from django.contrib import admin
from django.urls import path, include
from restaurante_app.views import inicio
from restaurante_app import views 
from django.contrib.auth.views import LogoutView
from restaurante_app.views import profile
from restaurante_app.views import lista_mesas, abrir_mesa
from restaurante_app.views import crear_comanda, ver_comandas

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
    path('lista_mesas/', views.lista_mesas, name='lista_mesas'),
    path('abrir_mesa/', views.abrir_mesa, name='abrir_mesa'),
    path('cerrar_mesa/<int:mesa_id>/', views.cerrar_mesa, name='cerrar_mesa'),
    path('crear_comanda/', crear_comanda, name='crear_comanda'),
    path('ver_comandas/', ver_comandas, name='ver_comandas'),
    
   
    
]
