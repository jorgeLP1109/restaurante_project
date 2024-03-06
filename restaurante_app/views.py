# restaurante_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Producto, Ticket, Cliente
from .forms import ProductoForm
from .forms import ClienteForm
from django.urls import reverse
from .models import Mesa, Comanda, Contabilidad
from .forms import MesaForm
from .forms import ComandaForm
from django.http import JsonResponse
from datetime import datetime

def agregar_comanda(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    productos = Producto.objects.all()  # Obtén todos los productos, puedes ajustar esto según tus necesidades

    if request.method == 'POST':
        producto_id = request.POST.get('producto_id')
        cantidad = request.POST.get('cantidad')

        if producto_id and cantidad:
            producto = get_object_or_404(Producto, id=producto_id)
            comanda, created = Comanda.objects.get_or_create(mesa=mesa, producto=producto)
            comanda.cantidad += int(cantidad)
            comanda.save()

    comandas = Comanda.objects.filter(mesa=mesa)

    return render(request, 'restaurante_app/agregar_comanda.html', {'mesa': mesa, 'productos': productos, 'comandas': comandas})

def crear_comanda(request):
    if request.method == 'POST':
        form = ComandaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_mesas')  # Redirige a donde desees después de crear la comanda
    else:
        form = ComandaForm()

    return render(request, 'restaurante_app/crear_comanda.html', {'form': form})

def ver_comandas(request):
    comandas = Comanda.objects.all()
    return render(request, 'restaurante_app/ver_comandas.html', {'comandas': comandas})

def lista_mesas(request):
    mesas = Mesa.objects.all()
    return render(request, 'restaurante_app/lista_mesas.html', {'mesas': mesas})

def abrir_mesa(request):
    if request.method == 'POST':
        form = MesaForm(request.POST)
        if form.is_valid():
            mesa = form.save()
            return redirect('lista_mesas')
    else:
        form = MesaForm()
    return render(request, 'restaurante_app/abrir_mesa.html', {'form': form})

'''def cerrar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    comandas = Comanda.objects.filter(mesa=mesa)
    total = sum(comanda.producto.precio * comanda.cantidad for comanda in comandas)

    contabilidad, created = Contabilidad.objects.get_or_create(fecha_cierre__date=datetime.date.today())
    contabilidad.total_diario += total
    contabilidad.save()

    # Eliminar la mesa y comandas
    mesa.delete()
    comandas.delete()

    #return render(request, 'restaurante_app/cerrar_mesa.html', {'mesa': mesa, 'comandas': comandas, 'total': total})

    return JsonResponse({'success': True, 'total': total})
'''
def cerrar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    comandas = Comanda.objects.filter(mesa=mesa)
    total = sum(comanda.producto.precio * comanda.cantidad for comanda in comandas)

    # Lógica para cerrar la mesa
    contabilidad = Contabilidad.objects.last()  # Obtén la última instancia de Contabilidad
    if not contabilidad or contabilidad.fecha_cierre.date() != datetime.now().date():
        # Si no hay contabilidad para hoy, crea una nueva instancia de Contabilidad
        contabilidad = Contabilidad.objects.create()

    # Actualiza el total diario
    contabilidad.total_diario += total
    contabilidad.save()

    # Elimina la mesa de la lista
    mesa.delete()

    return render(request, 'restaurante_app/cerrar_mesa.html', {'mesa': mesa, 'comandas': comandas, 'total': total})

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

