from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from .models import Venta, Producto, Compra

# ==================== VISTA DE INICIO ====================
@login_required(login_url='login')
def inicio(request):
    """Vista protegida de inicio. Requiere estar autenticado."""
    return render(request, 'inicio.html')


# ==================== VISTAS PARA VENTAS ====================
@login_required(login_url='login')
@permission_required('inventario.view_venta', raise_exception=True)
@require_http_methods(["GET"])
def ver_ventas(request):
    """Ver todas las ventas. Requiere permiso de visualización."""
    ventas = Venta.objects.all()
    context = {'ventas': ventas}
    return render(request, 'ventas.html', context)


@login_required(login_url='login')
@permission_required('inventario.add_venta', raise_exception=True)
@require_http_methods(["GET", "POST"])
def agregar_venta(request):
    """Agregar nueva venta. Requiere permiso de creación."""
    if request.method == 'POST':
        # Procesar formulario
        pass
    return render(request, 'agregar_venta.html')


@login_required(login_url='login')
@permission_required('inventario.change_venta', raise_exception=True)
@require_http_methods(["GET", "POST"])
def editar_venta(request, id):
    """Editar venta existente. Requiere permiso de modificación."""
    venta = get_object_or_404(Venta, id=id)
    if request.method == 'POST':
        # Procesar formulario
        pass
    context = {'venta': venta}
    return render(request, 'editar_venta.html', context)


@login_required(login_url='login')
@permission_required('inventario.delete_venta', raise_exception=True)
@require_http_methods(["GET", "POST"])
def eliminar_venta(request, id):
    """Eliminar venta. Requiere permiso de eliminación."""
    venta = get_object_or_404(Venta, id=id)
    if request.method == 'POST':
        venta.delete()
        # Redirigir a lista de ventas
    context = {'venta': venta}
    return render(request, 'eliminar_venta.html', context)


# ==================== VISTAS PARA PRODUCTOS ====================
@login_required(login_url='login')
@permission_required('inventario.view_producto', raise_exception=True)
@require_http_methods(["GET"])
def ver_productos(request):
    """Ver todos los productos. Requiere permiso de visualización."""
    productos = Producto.objects.all()
    context = {'productos': productos}
    return render(request, 'productos.html', context)


@login_required(login_url='login')
@permission_required('inventario.add_producto', raise_exception=True)
@require_http_methods(["GET", "POST"])
def agregar_producto(request):
    """Agregar nuevo producto. Requiere permiso de creación."""
    if request.method == 'POST':
        # Procesar formulario
        pass
    return render(request, 'agregar_producto.html')


@login_required(login_url='login')
@permission_required('inventario.change_producto', raise_exception=True)
@require_http_methods(["GET", "POST"])
def editar_producto(request, id):
    """Editar producto existente. Requiere permiso de modificación."""
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        # Procesar formulario
        pass
    context = {'producto': producto}
    return render(request, 'editar_producto.html', context)


@login_required(login_url='login')
@permission_required('inventario.delete_producto', raise_exception=True)
@require_http_methods(["GET", "POST"])
def eliminar_producto(request, id):
    """Eliminar producto. Requiere permiso de eliminación."""
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.delete()
        # Redirigir a lista de productos
    context = {'producto': producto}
    return render(request, 'eliminar_producto.html', context)


# ==================== VISTAS PARA COMPRAS ====================
@login_required(login_url='login')
@permission_required('inventario.view_compra', raise_exception=True)
@require_http_methods(["GET"])
def ver_compras(request):
    """Ver todas las compras. Requiere permiso de visualización."""
    compras = Compra.objects.all()
    context = {'compras': compras}
    return render(request, 'compras.html', context)


@login_required(login_url='login')
@permission_required('inventario.add_compra', raise_exception=True)
@require_http_methods(["GET", "POST"])
def agregar_compra(request):
    """Agregar nueva compra. Requiere permiso de creación."""
    if request.method == 'POST':
        # Procesar formulario
        pass
    return render(request, 'agregar_compra.html')


@login_required(login_url='login')
@permission_required('inventario.change_compra', raise_exception=True)
@require_http_methods(["GET", "POST"])
def editar_compra(request, id):
    """Editar compra existente. Requiere permiso de modificación."""
    compra = get_object_or_404(Compra, id=id)
    if request.method == 'POST':
        # Procesar formulario
        pass
    context = {'compra': compra}
    return render(request, 'editar_compra.html', context)


@login_required(login_url='login')
@permission_required('inventario.delete_compra', raise_exception=True)
@require_http_methods(["GET", "POST"])
def eliminar_compra(request, id):
    """Eliminar compra. Requiere permiso de eliminación."""
    compra = get_object_or_404(Compra, id=id)
    if request.method == 'POST':
        compra.delete()
        # Redirigir a lista de compras
    context = {'compra': compra}
    return render(request, 'eliminar_compra.html', context)

# ==================== CRUD VENTAS ====================

from .forms import VentaForm
from django.shortcuts import redirect

#AGREGAR VENTA
@login_required(login_url='login')
@permission_required('inventario.add_venta', raise_exception=True)
@require_http_methods(["GET", "POST"])
def agregar_venta(request):
    
    """Agregar nueva venta. Requiere permiso de creación."""
    
    if request.method == 'POST':
        form = VentaForm(request.POST)
        if form.is_valid():
            venta = form.save(commit=False)
            venta.usuario = request.user 
            venta.save() 
            return redirect('ver_ventas')
    else:
        form = VentaForm()
    return render(request, 'agregar_venta.html', {'form': form}) 

#EDITAR VENTA
@login_required(login_url='login')
@permission_required('inventario.change_venta', raise_exception=True)
@require_http_methods(["GET", "POST"])
def editar_venta(request, id):
    
    """Editar venta existente. Requiere permiso de modificación."""
    
    venta = get_object_or_404(Venta, id=id)
    if request.method == 'POST':
        form = VentaForm(request.POST, instance=venta)
        if form.is_valid():
            form.save()
            return redirect('ver_ventas')
    else:
        form = VentaForm(instance=venta)
    context = {'form': form, 'venta': venta}
    return render(request, 'editar_venta.html', context)

#ELIMINAR VENTA
@login_required(login_url='login')
@permission_required('inventario.delete_venta', raise_exception=True)
@require_http_methods(["GET", "POST"])
def eliminar_venta(request, id):
    
    """Eliminar venta. Requiere permiso de eliminación."""
    
    venta = get_object_or_404(Venta, id=id)
    if request.method == 'POST':
        venta.delete()
        return redirect('ver_ventas')
    context = {'venta': venta}
    return render(request, 'eliminar_venta.html', context)