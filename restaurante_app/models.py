# en el archivo models.py de tu aplicación (restaurante_app/models.py)

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User, Group

class Contabilidad(models.Model):
    fecha_cierre = models.DateTimeField(default=timezone.now)
    total_diario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f'Contabilidad - {self.fecha_cierre.date()}'

class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.nombre


class Ticket(models.Model):
    codigo = models.CharField(max_length=20, unique=True)
    fecha_emision = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    # Agrega más atributos según tus necesidades

    def __str__(self):
        return f'Ticket {self.codigo}'

class PerfilUsuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    grupo = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username
    
class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nombre

class Mesa(models.Model):
    nombre = models.CharField(max_length=100)
    abierta = models.BooleanField(default=False)
    cliente_nombre = models.CharField(max_length=100, blank=True, null=True)
    cliente_identificacion = models.CharField(max_length=20, blank=True, null=True)
    total_diario = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.nombre

class Comanda(models.Model):
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.producto.nombre} - {self.cantidad}"

class Cuenta(models.Model):
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    productos = models.ManyToManyField(Producto, through='ItemCuenta')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Cuenta de la Mesa {self.mesa.numero}"

class ItemCuenta(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cuenta = models.ForeignKey(Cuenta, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

class Bebida(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    cantidad_disponible = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre
