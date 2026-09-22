# tienda/forms.py
from django import forms
from .models import Cliente, Mascota, Producto, Cita


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '👤 Nombre del Cliente'
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '📞 Teléfono de Contacto'
            }),
            'direccion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '🏠 Dirección'
            }),
        }


class MascotaForm(forms.ModelForm):
    class Meta:
        model = Mascota
        fields = ['nombre', 'especie', 'raza', 'edad', 'cliente']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '🐾 Nombre de la Mascota'
            }),
            'especie': forms.Select(attrs={'class': 'form-select'}),
            'raza': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '🐕 Especie / Raza'
            }),
            'edad': forms.NumberInput(attrs={'class': 'form-control'}),
            'cliente': forms.Select(attrs={'class': 'form-select'}),
        }


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'stock']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '📦 Nombre del Producto'
            }),
            'precio': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '💲 Precio (COP)'
            }),
            'stock': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': '📊 Stock Inicial'
            }),
        }


class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['cliente', 'mascota', 'servicio', 'fecha_hora', 'estado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-select'}),
            'mascota': forms.Select(attrs={'class': 'form-select'}),
            'servicio': forms.Select(attrs={'class': 'form-select'}),
            'fecha_hora': forms.DateTimeInput(attrs={
                'class': 'form-control',
                'type': 'datetime-local'
            }),
            'estado': forms.Select(attrs={'class': 'form-select'}),
        }