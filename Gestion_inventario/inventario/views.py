from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db import transaction
from django.db.models import F
from .models import (Venta, Producto, Compra, Cliente, Proveedor, 
                     DetalleVenta, DetalleCompra)
from .forms import (VentaForm, CompraForm, ClienteForm, ProveedorForm, 
                   ProductoForm, DetalleVentaFormSet, DetalleCompraFormSet,
                   DetalleVentaForm, DetalleCompraForm)

# ==================== VISTA DE INICIO ====================
@login_required(login_url='login')
def inicio(request):
    """Vista protegida de inicio. Requiere estar autenticado."""
    contexto = {
        'total_productos': Producto.objects.count(),
        'total_clientes': Cliente.objects.count(),
        'total_proveedores': Proveedor.objects.count(),
        'total_ventas': Venta.objects.count(),
        'total_compras': Compra.objects.count(),
        'productos_bajo_stock': Producto.objects.filter(stock__lte=F('stock_minimo')).count(),
    }
    return render(request, 'inicio.html', contexto)


# ==================== VISTAS PARA CLIENTES ====================
@login_required(login_url='login')
@permission_required('inventario.view_cliente', raise_exception=True)
@require_http_methods(["GET"])
def ver_clientes(request):
    """Ver todos los clientes."""
    clientes = Cliente.objects.all()
    contexto = {'clientes': clientes}
    return render(request, 'clientes.html', contexto)


@login_required(login_url='login')
@permission_required('inventario.add_cliente', raise_exception=True)
@require_http_methods(["GET", "POST"])
def agregar_cliente(request):
    """Agregar nuevo cliente."""
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente agregado exitosamente.')
            return redirect('ver_clientes')
    else:
        form = ClienteForm()
    return render(request, 'agregar_cliente.html', {'form': form})


@login_required(login_url='login')
@permission_required('inventario.change_cliente', raise_exception=True)
@require_http_methods(["GET", "POST"])
def editar_cliente(request, id):
    """Editar cliente existente."""
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cliente actualizado exitosamente.')
            return redirect('ver_clientes')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'editar_cliente.html', {'form': form, 'cliente': cliente})


@login_required(login_url='login')
@permission_required('inventario.delete_cliente', raise_exception=True)
@require_http_methods(["GET", "POST"])
def eliminar_cliente(request, id):
    """Eliminar cliente."""
    cliente = get_object_or_404(Cliente, id=id)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente eliminado exitosamente.')
        return redirect('ver_clientes')
    return render(request, 'eliminar_cliente.html', {'cliente': cliente})


# ==================== VISTAS PARA PROVEEDORES ====================
@login_required(login_url='login')
@permission_required('inventario.view_proveedor', raise_exception=True)
@require_http_methods(["GET"])
def ver_proveedores(request):
    """Ver todos los proveedores."""
    proveedores = Proveedor.objects.all()
    contexto = {'proveedores': proveedores}
    return render(request, 'proveedores.html', contexto)


@login_required(login_url='login')
@permission_required('inventario.add_proveedor', raise_exception=True)
@require_http_methods(["GET", "POST"])
def agregar_proveedor(request):
    """Agregar nuevo proveedor."""
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor agregado exitosamente.')
            return redirect('ver_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'agregar_proveedor.html', {'form': form})


@login_required(login_url='login')
@permission_required('inventario.change_proveedor', raise_exception=True)
@require_http_methods(["GET", "POST"])
def editar_proveedor(request, id):
    """Editar proveedor existente."""
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=proveedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Proveedor actualizado exitosamente.')
            return redirect('ver_proveedores')
    else:
        form = ProveedorForm(instance=proveedor)
    return render(request, 'editar_proveedor.html', {'form': form, 'proveedor': proveedor})


@login_required(login_url='login')
@permission_required('inventario.delete_proveedor', raise_exception=True)
@require_http_methods(["GET", "POST"])
def eliminar_proveedor(request, id):
    """Eliminar proveedor."""
    proveedor = get_object_or_404(Proveedor, id=id)
    if request.method == 'POST':
        proveedor.delete()
        messages.success(request, 'Proveedor eliminado exitosamente.')
        return redirect('ver_proveedores')
    return render(request, 'eliminar_proveedor.html', {'proveedor': proveedor})


# ==================== VISTAS PARA PRODUCTOS ====================
@login_required(login_url='login')
@permission_required('inventario.view_producto', raise_exception=True)
@require_http_methods(["GET"])
def ver_productos(request):
    """Ver todos los productos."""
    productos = Producto.objects.all()
    contexto = {'productos': productos}
    return render(request, 'productos.html', contexto)


@login_required(login_url='login')
@permission_required('inventario.add_producto', raise_exception=True)
@require_http_methods(["GET", "POST"])
def agregar_producto(request):
    """Agregar nuevo producto."""
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto agregado exitosamente.')
            return redirect('ver_productos')
    else:
        form = ProductoForm()
    return render(request, 'agregar_producto.html', {'form': form})


@login_required(login_url='login')
@permission_required('inventario.change_producto', raise_exception=True)
@require_http_methods(["GET", "POST"])
def editar_producto(request, id):
    """Editar producto existente."""
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado exitosamente.')
            return redirect('ver_productos')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'editar_producto.html', {'form': form, 'producto': producto})


@login_required(login_url='login')
@permission_required('inventario.delete_producto', raise_exception=True)
@require_http_methods(["GET", "POST"])
def eliminar_producto(request, id):
    """Eliminar producto."""
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        messages.success(request, 'Producto eliminado exitosamente.')
        return redirect('ver_productos')
    return render(request, 'eliminar_producto.html', {'producto': producto})


# ==================== VISTAS PARA VENTAS ====================
@login_required(login_url='login')
@permission_required('inventario.view_venta', raise_exception=True)
@require_http_methods(["GET"])
def ver_ventas(request):
    """Ver todas las ventas."""
    ventas = Venta.objects.all()
    contexto = {'ventas': ventas}
    return render(request, 'ventas.html', contexto)


@login_required(login_url='login')
@permission_required('inventario.add_venta', raise_exception=True)
@require_http_methods(["GET", "POST"])
def agregar_venta(request):
    """Agregar nueva venta con detalles."""
    if request.method == 'POST':
        form = VentaForm(request.POST)
        formset = DetalleVentaFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                venta = form.save(commit=False)
                venta.usuario = request.user
                venta.save()
                
                # Guardar detalles y actualizar stock
                for detalle_form in formset:
                    if detalle_form.cleaned_data and not detalle_form.cleaned_data.get('DELETE', False):
                        detalle = detalle_form.save(commit=False)
                        detalle.venta = venta
                        detalle.save()
                        
                        # Actualizar stock del producto
                        producto = detalle.producto
                        producto.stock -= detalle.cantidad
                        producto.save()
                
                messages.success(request, 'Venta agregada exitosamente.')
                return redirect('ver_ventas')
    else:
        form = VentaForm()
        formset = DetalleVentaFormSet()
    
    return render(request, 'agregar_venta.html', {'form': form, 'formset': formset})


@login_required(login_url='login')
@permission_required('inventario.change_venta', raise_exception=True)
@require_http_methods(["GET", "POST"])
def editar_venta(request, id):
    """Editar venta existente."""
    venta = get_object_or_404(Venta, id=id)
    
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        formset = DetalleVentaFormSet(request.POST, instance=venta)
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                
                # Restaurar stock anterior
                for detalle in venta.detalles.all():
                    detalle.producto.stock += detalle.cantidad
                    detalle.producto.save()
                
                # Guardar nuevos detalles y actualizar stock
                formset.save()
                for detalle_form in formset:
                    if detalle_form.cleaned_data and not detalle_form.cleaned_data.get('DELETE', False):
                        detalle = detalle_form.instance
                        detalle.producto.stock -= detalle.cantidad
                        detalle.producto.save()
                
                messages.success(request, 'Venta actualizada exitosamente.')
                return redirect('ver_ventas')
    else:
        form = VentaForm(instance=venta)
        formset = DetalleVentaFormSet(instance=venta)
    
    return render(request, 'editar_venta.html', {'form': form, 'formset': formset, 'venta': venta})


@login_required(login_url='login')
@permission_required('inventario.delete_venta', raise_exception=True)
@require_http_methods(["GET", "POST"])
def eliminar_venta(request, id):
    """Eliminar venta."""
    venta = get_object_or_404(Venta, id=id)
    
    if request.method == 'POST':
        # Restaurar stock
        for detalle in venta.detalles.all():
            detalle.producto.stock += detalle.cantidad
            detalle.producto.save()
        
        venta.delete()
        messages.success(request, 'Venta eliminada exitosamente.')
        return redirect('ver_ventas')
    
    return render(request, 'eliminar_venta.html', {'venta': venta})


# ==================== VISTAS PARA COMPRAS ====================
@login_required(login_url='login')
@permission_required('inventario.view_compra', raise_exception=True)
@require_http_methods(["GET"])
def ver_compras(request):
    """Ver todas las compras."""
    compras = Compra.objects.all()
    contexto = {'compras': compras}
    return render(request, 'compras.html', contexto)


@login_required(login_url='login')
@permission_required('inventario.add_compra', raise_exception=True)
@require_http_methods(["GET", "POST"])
def agregar_compra(request):
    """Agregar nueva compra con detalles."""
    if request.method == 'POST':
        form = CompraForm(request.POST)
        formset = DetalleCompraFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                compra = form.save(commit=False)
                compra.usuario = request.user
                compra.save()
                
                # Guardar detalles y actualizar stock
                for detalle_form in formset:
                    if detalle_form.cleaned_data and not detalle_form.cleaned_data.get('DELETE', False):
                        detalle = detalle_form.save(commit=False)
                        detalle.compra = compra
                        detalle.save()
                        
                        # Actualizar stock del producto
                        producto = detalle.producto
                        producto.stock += detalle.cantidad
                        producto.save()
                
                messages.success(request, 'Compra agregada exitosamente.')
                return redirect('ver_compras')
    else:
        form = CompraForm()
        formset = DetalleCompraFormSet()
    
    return render(request, 'agregar_compra.html', {'form': form, 'formset': formset})


@login_required(login_url='login')
@permission_required('inventario.change_compra', raise_exception=True)
@require_http_methods(["GET", "POST"])
def editar_compra(request, id):
    """Editar compra existente."""
    compra = get_object_or_404(Compra, id=id)
    
    if request.method == 'POST':
        form = CompraForm(request.POST, instance=compra)
        formset = DetalleCompraFormSet(request.POST, instance=compra)
        
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                
                # Restaurar stock anterior
                for detalle in compra.detalles.all():
                    detalle.producto.stock -= detalle.cantidad
                    detalle.producto.save()
                
                # Guardar nuevos detalles y actualizar stock
                formset.save()
                for detalle_form in formset:
                    if detalle_form.cleaned_data and not detalle_form.cleaned_data.get('DELETE', False):
                        detalle = detalle_form.instance
                        detalle.producto.stock += detalle.cantidad
                        detalle.producto.save()
                
                messages.success(request, 'Compra actualizada exitosamente.')
                return redirect('ver_compras')
    else:
        form = CompraForm(instance=compra)
        formset = DetalleCompraFormSet(instance=compra)
    
    return render(request, 'editar_compra.html', {'form': form, 'formset': formset, 'compra': compra})


@login_required(login_url='login')
@permission_required('inventario.delete_compra', raise_exception=True)
@require_http_methods(["GET", "POST"])
def eliminar_compra(request, id):
    """Eliminar compra."""
    compra = get_object_or_404(Compra, id=id)
    
    if request.method == 'POST':
        # Restaurar stock
        for detalle in compra.detalles.all():
            detalle.producto.stock -= detalle.cantidad
            detalle.producto.save()
        
        compra.delete()
        messages.success(request, 'Compra eliminada exitosamente.')
        return redirect('ver_compras')
    
    return render(request, 'eliminar_compra.html', {'compra': compra})