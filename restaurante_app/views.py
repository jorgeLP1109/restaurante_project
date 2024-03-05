# restaurante_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Producto, Ticket, Cliente
from .forms import ProductoForm
from .forms import ClienteForm
from django.urls import reverse


def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            # Guardar el producto si el formulario es válido
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm()

    return render(request, 'restaurante_app/agregar_producto.html', {'form': form})

def listar_clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'restaurante_app/listar_clientes.html', {'clientes': clientes})

def detalle_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    return render(request, 'restaurante_app/detalle_cliente.html', {'cliente': cliente})

def agregar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm()
    return render(request, 'restaurante_app/agregar_cliente.html', {'form': form})

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('listar_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'restaurante_app/editar_cliente.html', {'form': form, 'cliente': cliente})

def eliminar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    cliente.delete()
    return redirect('listar_clientes')


def cargar_editar_producto(request, pk=None):
    if pk:
        producto = get_object_or_404(Producto, pk=pk)
    else:
        producto = None

    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('admin_interface')  # Cambia 'admin_interface' por la URL correcta
    else:
        form = ProductoForm(instance=producto)

    return render(request, 'restaurante_app/cargar_editar_producto.html', {'form': form})

def admin_interface(request):
    productos = Producto.objects.all()
    tickets = Ticket.objects.all()
    Cliente = Cliente.objects.all()

    return render(request, 'restaurante_app/admin_interface.html', {
        'productos': productos,
        'tickets': tickets,
        'Cliente': Cliente,
    })

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



@login_required
def profile(request):
    return render(request, 'restaurante_app/profile.html')


@login_required
def ver_perfil(request):
    # Aquí puedes agregar lógica para obtener información adicional del usuario si es necesario
    return render(request, 'restaurante_app/profile.html')

def lista_productos(request):
    productos = Producto.objects.all()  # Obtener todos los productos
    return render(request, 'restaurante_app/lista_productos.html', {'productos': productos})

def editar_producto(request, pk):
    producto = get_object_or_404(Producto, id=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            return redirect('lista_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'restaurante_app/editar_producto.html', {'form': form})
    


def eliminar_producto(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    # Lógica para eliminar el producto
    producto.delete()
    return redirect('lista_productos')

