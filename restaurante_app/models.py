# en el archivo models.py de tu aplicación (restaurante_app/models.py)

from django.db import models
from django.contrib.auth.models import User, Group

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
    numero = models.IntegerField(unique=True)
    ocupada = models.BooleanField(default=False)

    def __str__(self):
        return f"Mesa {self.numero}"

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
