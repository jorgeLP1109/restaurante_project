# restaurante_app/forms.py
from django import forms
from .models import Producto
from .models import Cliente

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'descripcion']  # Ajusta según los campos de tu modelo


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'        
