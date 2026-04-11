from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Venta, Producto, Compra

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente']