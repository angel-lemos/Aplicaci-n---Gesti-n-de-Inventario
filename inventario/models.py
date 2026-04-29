from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver

#Creamos las clases para cada modelo de la base de datos, con sus respectivos campos y relaciones entre ellos
class Proveedor(models.Model):
    nombre_proveedor = models.CharField(max_length=100)
    telefono = models.CharField(max_length=9)
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=200)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['-activo', 'nombre_proveedor']
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'

    def __str__(self):
        return self.nombre_proveedor

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=9)
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=200)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['-activo', 'nombre']
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nombre

class Perfil(models.Model):
    ROLES = [
        ('administrador', 'Administrador'),
        ('empleado', 'Empleado'),
        ('invitado', 'Invitado'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    telefono = models.CharField(max_length=20, blank=True)
    rol = models.CharField(max_length=15, choices=ROLES, default='empleado')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['user__username']
        verbose_name = 'Perfil de Usuario'
        verbose_name_plural = 'Perfiles de Usuario'

    def __str__(self):
        return f"{self.user.username} ({self.get_rol_display()})"

    def save(self, *args, **kwargs):
        self.user.is_staff = self.rol == 'administrador'
        self.user.save(update_fields=['is_staff'])
        super().save(*args, **kwargs)

@receiver(post_save, sender=User)
def crear_perfil_usuario(sender, instance, created, **kwargs):
    if created:
        Perfil.objects.create(user=instance)

class Producto(models.Model):
    UNIDADES_MEDIDA = [
        ('kg', 'Kilogramos'),
        ('g', 'Gramos'),
        ('l', 'Litros'),
        ('ml', 'Mililitros'),
        ('m', 'Metros'),
        ('cm', 'Centímetros'),
        ('u', 'Unidad'),
        ('docena', 'Docena'),
        ('paquete', 'Paquete'),
        ('lata', 'Lata'),
        ('botella', 'Botella'),
        ('caja', 'Caja'),
    ]
    
    nombre_producto = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=0)
    unidad_medida = models.CharField(max_length=20, choices=UNIDADES_MEDIDA, default='u')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    class Meta:
        ordering = ['nombre_producto']
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return f"{self.nombre_producto} (Stock: {self.stock})"

    def stock_bajo(self):
        return self.stock <= self.stock_minimo
    
    def stock_critico_nivel(self):
        """Retorna True si el stock es crítico (5 o menos)"""
        return self.stock <= 5

class Compra(models.Model):
    ESTADO_COMPRA = [
        ('borrador', 'Borrador'),
        ('confirmada', 'Confirmada'),
        ('recibida', 'Recibida'),
        ('cancelada', 'Cancelada'),
    ]
    
    fecha_compra = models.DateField(auto_now_add=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name='compras')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='compras_realizadas')
    estado = models.CharField(max_length=20, choices=ESTADO_COMPRA, default='borrador')
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ['-fecha_compra']
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'

    def __str__(self):
        return f"Compra {self.id} - {self.proveedor} ({self.estado})"

    def calcular_total(self):
        return sum(detalle.subtotal() for detalle in self.detalles.all())

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='detalles_compra')
    cantidad = models.PositiveIntegerField()
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ['compra', 'producto']
        verbose_name = 'Detalle Compra'
        verbose_name_plural = 'Detalles Compra'

    def __str__(self):
        return f"Detalle Compra {self.compra.id} - {self.producto.nombre_producto}"

    def subtotal(self):
        return self.cantidad * self.precio_compra

class Venta(models.Model):
    ESTADO_VENTA = [
        ('borrador', 'Borrador'),
        ('confirmada', 'Confirmada'),
        ('entregada', 'Entregada'),
        ('cancelada', 'Cancelada'),
    ]
    
    fecha_venta = models.DateField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='ventas')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ventas_realizadas')
    estado = models.CharField(max_length=20, choices=ESTADO_VENTA, default='borrador')
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        ordering = ['-fecha_venta']
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        
    def __str__(self):
        return f"Venta {self.id} - {self.cliente} ({self.estado})"

    def calcular_total(self):
        return sum(detalle.subtotal() for detalle in self.detalles.all())

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT, related_name='detalles_venta')
    cantidad = models.PositiveIntegerField()
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ['venta', 'producto']
        verbose_name = 'Detalle Venta'
        verbose_name_plural = 'Detalles Venta'

    def __str__(self):
        return f"Detalle Venta {self.venta.id} - {self.producto.nombre_producto}"

    def subtotal(self):
        return self.cantidad * self.precio_venta
    
    def clean(self):
        if self.cantidad > self.producto.stock:
            raise ValidationError(f"No hay suficiente stock. Disponible: {self.producto.stock}")

class Reporte(models.Model):
    TIPOS_REPORTE = [
        ('inventario', 'Reporte de Inventario'),
        ('ventas', 'Reporte de Ventas'),
        ('compras', 'Reporte de Compras'),
    ]
    
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=20, choices=TIPOS_REPORTE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reportes_generados')
    fecha_generacion = models.DateTimeField(auto_now_add=True)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    contenido_json = models.JSONField(default=dict)
    
    class Meta:
        ordering = ['-fecha_generacion']
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'
    
    def __str__(self):
        return f"{self.titulo} - {self.usuario.username} ({self.fecha_generacion.strftime('%d/%m/%Y')})"