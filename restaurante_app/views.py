# restaurante_app/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import Ticket, Cliente
from .forms import ClienteForm
from django.urls import reverse
from .models import Mesa, Comanda, Contabilidad
from .forms import MesaForm
from django.http import JsonResponse
from datetime import datetime
from .forms import CerrarMesaForm
from django.db.models import Sum
from django.db.models import Q
from .forms import ComandaForm, BebidaForm, ComidaForm
from .models import Bebida, Articulo, Comanda, Comida
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from .models import Mesa, Bebida, Articulo, Comanda, Comida

def agregar_comanda(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    bebidas = Bebida.objects.all()
    comidas = Comida.objects.all()

    if request.method == 'POST':
        if 'form-bebida' in request.POST:
            bebida_id = request.POST.get('bebida_id')
            cantidad = request.POST.get('bebida_cantidad')
            print(f"Bebida ID: {bebida_id}, Cantidad: {cantidad}")
            if bebida_id and cantidad:
                bebida = get_object_or_404(Bebida, id=bebida_id)
                comanda_existente = Comanda.objects.filter(mesa=mesa, bebida=bebida).first()
                if comanda_existente:
                    comanda_existente.cantidad += int(cantidad)
                    comanda_existente.save()
                else:
                    Comanda.objects.create(mesa=mesa, bebida=bebida, cantidad=int(cantidad))
        
        elif 'form-comida' in request.POST:
            comida_id = request.POST.get('comida_id')
            cantidad = request.POST.get('comida_cantidad')
            print(f"Comida ID: {comida_id}, Cantidad: {cantidad}")        
            if comida_id and cantidad:
                comida = get_object_or_404(Comida, id=comida_id)
                comanda_existente = Comanda.objects.filter(mesa=mesa, comida=comida).first()
                if comanda_existente:
                    comanda_existente.cantidad += int(cantidad)
                    comanda_existente.save()
                else:
                    Comanda.objects.create(mesa=mesa, comida=comida, cantidad=int(cantidad))

    comandas = Comanda.objects.filter(mesa=mesa)
    return render(request, 'restaurante_app/agregar_comanda.html', {'mesa': mesa,'bebidas': bebidas,'comidas': comidas, 'comandas': comandas})

def agregar_bebida(request):
    if request.method == 'POST':
        form = BebidaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventario')
    else:
        form = BebidaForm()
    return render(request, 'restaurante_app/agregar_bebida.html', {'form': form})

def agregar_comida(request):
    if request.method == 'POST':
        form = ComidaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = ComidaForm()
    return render(request, 'restaurante_app/agregar_comida.html', {'form': form})    



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


def cerrar_mesa(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    comandas = Comanda.objects.filter(mesa=mesa)
    
    # Calcular el total como un Decimal en lugar de un float
    total = Decimal(sum(comanda.bebida.precio * comanda.cantidad if comanda.bebida else
                        comanda.comida.precio * comanda.cantidad if comanda.comida else
                        comanda.articulo.precio * comanda.cantidad if comanda.articulo else 0 
                        for comanda in comandas))

    # Lógica para cerrar la mesa
    contabilidad = Contabilidad.objects.last()  # Obtén la última instancia de Contabilidad
    if not contabilidad or contabilidad.fecha_cierre.date() != datetime.now().date():
        # Si no hay contabilidad para hoy, crea una nueva instancia de Contabilidad
        contabilidad = Contabilidad.objects.create()

    # Actualiza el total diario
    contabilidad.total_diario += total
    contabilidad.save()

    # Elimina la mesa y comandas
    mesa.delete()
    comandas.delete()

    # Renderiza la plantilla con el detalle de la mesa cerrada
    return render(request, 'restaurante_app/cerrar_mesa_detalle.html', {'mesa': mesa, 'total': total})

#0joooooooooooooooooooooooooooooooooo!!!!!!!!! solo producto aqui
def cerrar_mesa_detalle(request, mesa_id):
    mesa = get_object_or_404(Mesa, id=mesa_id)
    comandas = Comanda.objects.filter(mesa=mesa)
    total = sum(comanda.producto.precio * comanda.cantidad for comanda in comandas)

    mesas_abiertas = Mesa.objects.filter(abierta=True)  # Obtener las mesas abiertas

    # Print out the comandas queryset to debug
    print(comandas)

    
    return render(request, 'restaurante_app/cerrar_mesa_detalle.html', {'mesa': mesa, 'comandas': comandas, 'total': total, 'mesas_abiertas': mesas_abiertas})

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

def admin_interface(request):
    tickets = Ticket.objects.all()
    Cliente = Cliente.objects.all()

    return render(request, 'restaurante_app/admin_interface.html', {
    
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

def consultar_contabilidad(request):
    # Obtener parámetros de consulta
    year = request.GET.get('year')
    month = request.GET.get('month')
    day = request.GET.get('day')

    # Filtrar los registros de contabilidad según los parámetros de consulta
    contabilidad = Contabilidad.objects.all()

    if year:
        contabilidad = contabilidad.filter(fecha_cierre__year=year)
    if month:
        contabilidad = contabilidad.filter(fecha_cierre__month=month)
    if day:
        contabilidad = contabilidad.filter(fecha_cierre__day=day)

    # Calcular el total sumando los valores de los registros filtrados
    total = contabilidad.aggregate(total=Sum('total_diario'))['total']

    # Si no hay registros, establecer el total en cero
    if total is None:
        total = 0

    return render(request, 'restaurante_app/contabilidad.html', {'contabilidad': contabilidad, 'total': total})

def contabilidad(request):
    contabilidad = Contabilidad.objects.all()

    # Filtro por año
    year = request.GET.get('year')
    if year:
        contabilidad = contabilidad.filter(fecha_cierre__year=year)

    # Filtro por mes
    month = request.GET.get('month')
    if month:
        contabilidad = contabilidad.filter(fecha_cierre__month=month)

    # Filtro por día
    day = request.GET.get('day')
    if day:
        contabilidad = contabilidad.filter(fecha_cierre__day=day)

    # Calcular el total general
    total_general = Contabilidad.objects.aggregate(total_general=Sum('total_diario'))['total_general'] or 0

    context = {
        'contabilidad': contabilidad,
        'total_general': total_general
    }

    return render(request, 'contabilidad.html', context)

def inventario(request):
    bebidas = Bebida.objects.all()
    return render(request, 'restaurante_app/inventario.html', {'bebidas': bebidas})

def menu(request):
    comidas = Comida.objects.all()
    return render(request, 'restaurante_app/menu.html', {'comidas': comidas})    


def editar_bebida(request, bebida_id):
    bebida = get_object_or_404(Bebida, id=bebida_id)
    if request.method == 'POST':
        form = BebidaForm(request.POST, instance=bebida)
        if form.is_valid():
            form.save()
            return redirect('inventario')
    else:
        form = BebidaForm(instance=bebida)
    return render(request, 'restaurante_app/editar_bebida.html', {'form': form})

def eliminar_bebida(request, bebida_id):
    bebida = get_object_or_404(Bebida, id=bebida_id)
    bebida.delete()
    return redirect('inventario')


def editar_comida(request, bebida_id):
    comida = get_object_or_404(Comida, id=comida_id)
    if request.method == 'POST':
        form = ComidaForm(request.POST, instance=comida)
        if form.is_valid():
            form.save()
            return redirect('menu')
    else:
        form = ComidaForm(instance=comida)
    return render(request, 'restaurante_app/editar_comida.html', {'form': form})

def eliminar_comida(request, bebida_id):
    comida = get_object_or_404(Comida, id=comida_id)
    comida.delete()
    return redirect('menu')    
