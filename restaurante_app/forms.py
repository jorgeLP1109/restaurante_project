# restaurante_app/forms.py
from django import forms
from .models import Cliente
from .models import Mesa
from .models import Comanda
from .models import Bebida
from .models import Comida

class ComandaForm(forms.ModelForm):
    class Meta:
        model = Comanda
        fields = ['mesa', 'comida', 'bebida', 'cantidad']
        # Puedes personalizar los widgets, etiquetas, etc., según tus necesidades

class MesaForm(forms.ModelForm):
    class Meta:
        model = Mesa
        fields = ['nombre', 'cliente_nombre', 'cliente_identificacion']
        

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'    

class CerrarMesaForm(forms.Form):
    mesa = forms.ModelChoiceField(queryset=Mesa.objects.filter(abierta=True))   

class BebidaForm(forms.ModelForm):
    class Meta:
        model = Bebida
        fields = ['nombre', 'descripcion', 'cantidad_disponible', 'precio']

class ComidaForm(forms.ModelForm):
    class Meta:
        model = Comida
        fields = ['nombre', 'descripcion', 'cantidad_disponible', 'precio']                
        
            
