
from django.contrib import admin
from django.urls import path, include
from restaurante_app.views import inicio
from restaurante_app import views 
from django.contrib.auth.views import LogoutView
from restaurante_app.views import profile
from restaurante_app.views import lista_mesas, abrir_mesa
from restaurante_app.views import crear_comanda, ver_comandas, agregar_comanda, cerrar_mesa, cerrar_mesa_detalle
from restaurante_app.views import inventario, agregar_bebida, editar_bebida, eliminar_bebida, menu, agregar_comida, editar_comida, eliminar_comida
app_name = 'restaurante_app'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),    
    path('', views.inicio, name='inicio'),
    
    path('registrar_usuario/', views.registrar_usuario, name='registrar_usuario'),
    path('cerrar_sesion/', LogoutView.as_view(), name='cerrar_sesion'),
    path('accounts/profile/', profile, name='profile'),
    path('perfil/', views.ver_perfil, name='ver_perfil'),
   
    
    
    path('lista_mesas/', views.lista_mesas, name='lista_mesas'),
    path('abrir_mesa/', views.abrir_mesa, name='abrir_mesa'),
    path('cerrar_mesa/<int:mesa_id>/', views.cerrar_mesa, name='cerrar_mesa'),
    path('crear_comanda/', crear_comanda, name='crear_comanda'),
    path('ver_comandas/', ver_comandas, name='ver_comandas'),
    path('agregar_comanda/<int:mesa_id>/', agregar_comanda, name='agregar_comanda'),
    path('cerrar_mesa/<int:mesa_id>/', cerrar_mesa, name='cerrar_mesa'),
    path('consultar_contabilidad/', views.consultar_contabilidad, name='consultar_contabilidad'),
    path('inventario/', inventario, name='inventario'),
    path('agregar_bebida/', agregar_bebida, name='agregar_bebida'),
    path('editar_bebida/<int:bebida_id>/', editar_bebida, name='editar_bebida'),
    path('eliminar_bebida/<int:bebida_id>/', eliminar_bebida, name='eliminar_bebida'),
    path('menu/', menu, name='menu'), #intento 
    path('agregar_comida/', agregar_comida, name='agregar_comida'),
    path('editar_comida/<int:comida_id>/', editar_comida, name='editar_comida'),
    path('eliminar_comida/<int:comida_id>/', eliminar_comida, name='eliminar_comida'),
   
    
   
    
]
