from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import Venta, Producto, Compra, Cliente, Proveedor, DetalleVenta, DetalleCompra, Perfil

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'})
    )

# ====================== FORMULARIOS PARA CLIENTES ======================
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre', 'telefono', 'email', 'direccion']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del cliente'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
        }
        labels = {
            'nombre': 'Nombre',
            'telefono': 'Teléfono',
            'email': 'Correo Electrónico',
            'direccion': 'Dirección',
        }

# ====================== FORMULARIOS PARA PROVEEDORES ======================
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre_proveedor', 'telefono', 'email', 'direccion']
        widgets = {
            'nombre_proveedor': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del proveedor'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección'}),
        }
        labels = {
            'nombre_proveedor': 'Nombre',
            'telefono': 'Teléfono',
            'email': 'Correo Electrónico',
            'direccion': 'Dirección',
        }

# ====================== FORMULARIOS PARA USUARIOS ======================
class UsuarioForm(forms.ModelForm):
    telefono = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono'}),
        label='Teléfono'
    )
    rol = forms.ChoiceField(
        choices=Perfil.ROLES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Rol'
    )
    password1 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
        label='Contraseña'
    )
    password2 = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar contraseña'}),
        label='Confirmar Contraseña'
    )
    is_active = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Activo'
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_active']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Usuario'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
        }
        labels = {
            'username': 'Usuario',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo Electrónico',
            'is_active': 'Activo',
        }

    def __init__(self, *args, **kwargs):
        self.editing = kwargs.pop('editing', False)
        super().__init__(*args, **kwargs)
        if self.editing:
            self.fields['password1'].required = False
            self.fields['password2'].required = False
            self.fields['password1'].widget.attrs['placeholder'] = 'Dejar en blanco para no cambiar'
            self.fields['password2'].widget.attrs['placeholder'] = 'Dejar en blanco para no cambiar'

        profile = None
        if self.instance and hasattr(self.instance, 'perfil'):
            profile = self.instance.perfil
            self.fields['telefono'].initial = profile.telefono
            self.fields['rol'].initial = profile.rol
        elif 'initial' in kwargs:
            self.fields['rol'].initial = kwargs['initial'].get('rol', 'empleado')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if not self.editing and not password1:
            self.add_error('password1', 'Debes ingresar una contraseña.')

        if password1 and password1 != password2:
            self.add_error('password2', 'Las contraseñas no coinciden.')

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get('password1')
        if password:
            user.set_password(password)
        if commit:
            user.save()
            Perfil.objects.update_or_create(
                user=user,
                defaults={
                    'telefono': self.cleaned_data.get('telefono', ''),
                    'rol': self.cleaned_data.get('rol', 'empleado'),
                }
            )
        return user

# ====================== FORMULARIOS PARA PRODUCTOS ======================
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre_producto', 'codigo', 'descripcion', 'precio', 'stock', 'stock_minimo', 'activo']
        widgets = {
            'nombre_producto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre del producto'}),
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Código único'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Descripción del producto'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock actual'}),
            'stock_minimo': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Stock mínimo'}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'nombre_producto': 'Nombre del Producto',
            'codigo': 'Código',
            'descripcion': 'Descripción',
            'precio': 'Precio (€)',
            'stock': 'Stock Actual',
            'stock_minimo': 'Stock Mínimo',
            'activo': 'Producto Activo',
        }

# ====================== FORMULARIOS PARA VENTAS ======================
class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente', 'estado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'cliente': 'Cliente',
            'estado': 'Estado',
        }

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad', 'precio_venta']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad', 'min': '1'}),
            'precio_venta': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio venta', 'step': '0.01'}),
        }
        labels = {
            'producto': 'Producto',
            'cantidad': 'Cantidad',
            'precio_venta': 'Precio de Venta (€)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer los campos opcionales para permitir filas vacías
        self.fields['producto'].required = False
        self.fields['cantidad'].required = False
        self.fields['precio_venta'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        cantidad = cleaned_data.get('cantidad')
        precio_venta = cleaned_data.get('precio_venta')
        
        # Si todos están vacíos, está bien (fila vacía)
        if not producto and not cantidad and not precio_venta:
            return cleaned_data
        
        # Si algunos están llenos, todos deben estar llenos
        if producto or cantidad or precio_venta:
            if not producto:
                self.add_error('producto', 'El producto es requerido')
            if not cantidad:
                self.add_error('cantidad', 'La cantidad es requerida')
            if not precio_venta:
                self.add_error('precio_venta', 'El precio es requerido')
        
        return cleaned_data

DetalleVentaFormSet = forms.inlineformset_factory(
    Venta, DetalleVenta, form=DetalleVentaForm, extra=1, can_delete=True
)

# ====================== FORMULARIOS PARA COMPRAS ======================
class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['proveedor', 'estado']
        widgets = {
            'proveedor': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'proveedor': 'Proveedor',
            'estado': 'Estado',
        }

class DetalleCompraForm(forms.ModelForm):
    class Meta:
        model = DetalleCompra
        fields = ['producto', 'cantidad', 'precio_compra']
        widgets = {
            'producto': forms.Select(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Cantidad', 'min': '1'}),
            'precio_compra': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Precio compra', 'step': '0.01'}),
        }
        labels = {
            'producto': 'Producto',
            'cantidad': 'Cantidad',
            'precio_compra': 'Precio de Compra (€)',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer los campos opcionales para permitir filas vacías
        self.fields['producto'].required = False
        self.fields['cantidad'].required = False
        self.fields['precio_compra'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        producto = cleaned_data.get('producto')
        cantidad = cleaned_data.get('cantidad')
        precio_compra = cleaned_data.get('precio_compra')
        
        # Si todos están vacíos, está bien (fila vacía)
        if not producto and not cantidad and not precio_compra:
            return cleaned_data
        
        # Si algunos están llenos, todos deben estar llenos
        if producto or cantidad or precio_compra:
            if not producto:
                self.add_error('producto', 'El producto es requerido')
            if not cantidad:
                self.add_error('cantidad', 'La cantidad es requerida')
            if not precio_compra:
                self.add_error('precio_compra', 'El precio es requerido')
        
        return cleaned_data

DetalleCompraFormSet = forms.inlineformset_factory(
    Compra, DetalleCompra, form=DetalleCompraForm, extra=1, can_delete=True
)