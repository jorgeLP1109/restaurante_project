# restaurante_app/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import permission_required
from .models import Producto
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def registrar_usuario(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
    else:
        form = UserCreationForm()
    return render(request, 'restaurante_app/registrar_usuario.html', {'form': form})

def inicio(request):
    return render(request, 'restaurante_app/inicio.html')

@permission_required('restaurante_app.can_agregar_producto', login_url='login')
def agregar_producto(request):
    if request.method == 'POST':
        # Procesar el formulario si se envió uno
        # Aquí debes manejar la lógica para agregar un nuevo producto a la base de datos
        # Puedes acceder a los datos del formulario usando request.POST

        # Ejemplo:
        nombre = request.POST['nombre']
        descripcion = request.POST['descripcion']
        precio = request.POST['precio']

        # Crea el nuevo producto
        Producto.objects.create(nombre=nombre, descripcion=descripcion, precio=precio)

        # Redirige a alguna página de éxito o muestra un mensaje
        return redirect('pagina_de_exito')  # Ajusta la URL según tus necesidades

    # Si no es una solicitud POST, renderiza el formulario
    return render(request, 'restaurante_app/agregar_producto.html')  # Ajusta el nombre de la plantilla según tus necesidades
