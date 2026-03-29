from django.db import models
from django.contrib.auth.models import User

class Proveedor(models.Model):
    nombre_proveedor = models.CharField(max_length=100)
    telefono = models.CharField(max_length=9)
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre_proveedor

class Compra(models.Model):
    fecha_compra = models.DateField(auto_now_add=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Compra {self.id} - {self.proveedor}"

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=9)
    email = models.EmailField(unique=True)
    direccion = models.CharField(max_length=200)

    def __str__(self):
        return self.nombre

class Venta(models.Model):
    fecha_venta = models.DateField(auto_now_add=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
        
    def __str__(self):
        return f"Venta {self.id}"

class Producto(models.Model):
    nombre_producto = models.CharField(max_length=100)
    codigo = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField()
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    stock_minimo = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre_producto

class DetalleCompra(models.Model):
    compra = models.ForeignKey(Compra, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle Compra {self.compra.id} - {self.producto.nombre_producto}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle Venta {self.venta.id} - {self.producto.nombre_producto}"