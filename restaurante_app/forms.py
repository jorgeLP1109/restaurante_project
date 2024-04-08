# restaurante_app/forms.py
from django import forms
from .models import Producto
from .models import Cliente
from .models import Mesa
from .models import Comanda

class ComandaForm(forms.ModelForm):
    class Meta:
        model = Comanda
        fields = ['mesa', 'producto', 'cantidad']
        # Puedes personalizar los widgets, etiquetas, etc., según tus necesidades

class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['nombre', 'cliente_nombre', 'cliente_identificacion']
        
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'descripcion', 'precio']


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'    

class CerrarMesaForm(forms.Form):
    mesa = forms.ModelChoiceField(queryset=Mesa.objects.filter(abierta=True))        
        
            
