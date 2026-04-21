from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db import transaction
from django.db.models import F, Sum, Q
from .models import (Venta, Producto, Compra, Cliente, Proveedor, 

                    DetalleVenta, DetalleCompra, Perfil)
from .forms import (VentaForm, CompraForm, ClienteForm, ProveedorForm, 
                ProductoForm, DetalleVentaFormSet, DetalleCompraFormSet,
                DetalleVentaForm, DetalleCompraForm, UsuarioForm)
from .decorators import roles_permitidos, solo_empleado


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
    if request.user.is_staff:
        if request.user.is_superuser:
            contexto['total_usuarios'] = User.objects.count()
        else:
            contexto['total_usuarios'] = User.objects.filter(is_superuser=False).count()
    contexto['es_administrador'] = request.user.is_superuser or (hasattr(request.user, 'perfil') and request.user.perfil.rol == 'administrador')
    return render(request, 'inicio.html', contexto)

def logout_view(request):
    """Cerrar sesión del usuario."""
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')

def administrador_required(view_func):
    """Permite acceso a superusers y administradores."""
    return user_passes_test(
        lambda u: u.is_authenticated and (
            u.is_superuser or 
            (hasattr(u, 'perfil') and u.perfil.rol == 'administrador')
        ),
        login_url='login',
        redirect_field_name=None
    )(view_func)


# ==================== VISTAS PARA USUARIOS ====================
@login_required(login_url='login')
@administrador_required
@require_http_methods(["GET"])
def ver_usuarios(request):
    # Los superusers ven todos los usuarios; los admins normales ven solo no-superusers
    if request.user.is_superuser:
        usuarios = User.objects.select_related('perfil').all().order_by('username')
    else:
        usuarios = User.objects.select_related('perfil').filter(is_superuser=False).order_by('username')
    return render(request, 'usuarios.html', {'usuarios': usuarios})


@login_required(login_url='login')
@administrador_required
@require_http_methods(["GET", "POST"])
def agregar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario agregado exitosamente.')
            return redirect('ver_usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'agregar_usuario.html', {'form': form})


@login_required(login_url='login')
@administrador_required
@require_http_methods(["GET", "POST"])
def eliminar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    
    # Verificar permisos de eliminación
    if hasattr(usuario, 'perfil') and usuario.perfil.rol == 'administrador':
        # Solo superusers pueden eliminar administradores
        if not request.user.is_superuser:
            messages.error(request, 'No tienes permisos para eliminar administradores.')
            return redirect('ver_usuarios')
    # Los administradores pueden eliminar empleados (y otros roles)
    
    if request.method == 'POST':
        usuario.is_active = False
        usuario.save(update_fields=['is_active'])
        messages.success(request, 'Usuario desactivado exitosamente.')
        return redirect('ver_usuarios')
    return render(request, 'eliminar_usuario.html', {'usuario': usuario})


@login_required(login_url='login')
@administrador_required
@require_http_methods(["GET", "POST"])
def activar_usuario(request, id):
    usuario = get_object_or_404(User, id=id)
    
    # Verificar permisos (similar a eliminar)
    if hasattr(usuario, 'perfil') and usuario.perfil.rol == 'administrador':
        if not request.user.is_superuser:
            messages.error(request, 'No tienes permisos para activar administradores.')
            return redirect('ver_usuarios')
    
    if request.method == 'POST':
        usuario.is_active = True
        usuario.save(update_fields=['is_active'])
        messages.success(request, 'Usuario activado exitosamente.')
        return redirect('ver_usuarios')
    return render(request, 'activar_usuario.html', {'usuario': usuario})


# ==================== VISTAS PARA CLIENTES ====================
@login_required(login_url='login')
@administrador_required
@require_http_methods(["GET"])
def ver_clientes(request):
    """Ver todos los clientes."""
    clientes = Cliente.objects.all()
    contexto = {'clientes': clientes}
    return render(request, 'clientes.html', contexto)


@login_required(login_url='login')
@administrador_required
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
@administrador_required
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
@administrador_required
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
@administrador_required
@require_http_methods(["GET"])
def ver_proveedores(request):
    """Ver todos los proveedores."""
    proveedores = Proveedor.objects.all()
    contexto = {'proveedores': proveedores}
    return render(request, 'proveedores.html', contexto)


@login_required(login_url='login')
@administrador_required
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
@administrador_required
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
@administrador_required
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
@administrador_required
@require_http_methods(["GET"])
def ver_productos(request):
    """Ver todos los productos."""
    productos = Producto.objects.all()
    contexto = {'productos': productos}
    return render(request, 'productos.html', contexto)


@login_required(login_url='login')
@administrador_required
@require_http_methods(["GET"])
def ver_inventario(request):
    """Consultar inventario con búsqueda y detalle."""
    query = request.GET.get('q', '').strip()
    productos = Producto.objects.all()
    if query:
        productos = productos.filter(
            Q(nombre_producto__icontains=query) |
            Q(codigo__icontains=query) |
            Q(descripcion__icontains=query)
        )
    contexto = {'productos': productos, 'query': query}
    return render(request, 'inventario_consulta.html', contexto)


@login_required(login_url='login')
@administrador_required
@require_http_methods(["GET"])
def detalle_producto(request, id):
    producto = get_object_or_404(Producto, id=id)
    return render(request, 'producto_detalle.html', {'producto': producto})


@login_required(login_url='login')
@administrador_required
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
@administrador_required
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
@administrador_required
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
@roles_permitidos('empleado', 'administrador')
@require_http_methods(["GET"])
def ver_ventas(request):
    """Ver todas las ventas."""
    ventas = Venta.objects.all()
    contexto = {'ventas': ventas}
    return render(request, 'ventas.html', contexto)


@login_required(login_url='login')
@roles_permitidos('empleado', 'administrador')
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
                        
                        if producto.stock <= 5:
                            messages.warning(request, f'El producto "{producto.nombre_producto}" está bajo stock (stock actual: {producto.stock}).')
                
                messages.success(request, 'Venta agregada exitosamente.')
                return redirect('ver_ventas')
    else:
        form = VentaForm()
        formset = DetalleVentaFormSet()
    
    return render(request, 'agregar_venta.html', {'form': form, 'formset': formset})


@login_required(login_url='login')
@administrador_required
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
@administrador_required
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
@administrador_required
@require_http_methods(["GET"])
def ver_compras(request):
    """Ver todas las compras."""
    compras = Compra.objects.all()
    contexto = {'compras': compras}
    return render(request, 'compras.html', contexto)


@login_required(login_url='login')
@administrador_required
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
@administrador_required
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
@administrador_required
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


@login_required(login_url='login')
@administrador_required
@require_http_methods(["GET"])
def ver_movimientos(request):
    """Ver el historial de movimientos de inventario."""
    tipo = request.GET.get('tipo', '')
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')

    movimientos = []
    compras = Compra.objects.all()
    ventas = Venta.objects.all()

    if fecha_inicio:
        compras = compras.filter(fecha_compra__gte=fecha_inicio)
        ventas = ventas.filter(fecha_venta__gte=fecha_inicio)
    if fecha_fin:
        compras = compras.filter(fecha_compra__lte=fecha_fin)
        ventas = ventas.filter(fecha_venta__lte=fecha_fin)

    if tipo in ['entrada', '']:
        for compra in compras:
            for detalle in compra.detalles.all():
                movimientos.append({
                    'fecha': compra.fecha_compra,
                    'tipo': 'Entrada',
                    'producto': detalle.producto,
                    'cantidad': detalle.cantidad,
                    'usuario': compra.usuario,
                    'referencia': f'Compra #{compra.id}',
                })
    if tipo in ['salida', '']:
        for venta in ventas:
            for detalle in venta.detalles.all():
                movimientos.append({
                    'fecha': venta.fecha_venta,
                    'tipo': 'Salida',
                    'producto': detalle.producto,
                    'cantidad': detalle.cantidad,
                    'usuario': venta.usuario,
                    'referencia': f'Venta #{venta.id}',
                })

    movimientos.sort(key=lambda m: m['fecha'], reverse=True)
    contexto = {
        'movimientos': movimientos,
        'tipo': tipo,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
    }
    return render(request, 'movimientos.html', contexto)


@login_required(login_url='login')
@administrador_required
@require_http_methods(["GET"])
def ver_reportes(request):
    """Ver reportes generales del sistema."""
    tipo = request.GET.get('tipo', 'inventario')
    fecha_inicio = request.GET.get('fecha_inicio', '')
    fecha_fin = request.GET.get('fecha_fin', '')

    ventas = Venta.objects.all()
    compras = Compra.objects.all()
    productos = Producto.objects.all()

    if fecha_inicio:
        ventas = ventas.filter(fecha_venta__gte=fecha_inicio)
        compras = compras.filter(fecha_compra__gte=fecha_inicio)
    if fecha_fin:
        ventas = ventas.filter(fecha_venta__lte=fecha_fin)
        compras = compras.filter(fecha_compra__lte=fecha_fin)

    total_ventas = sum(v.calcular_total() for v in ventas)
    total_compras = sum(c.calcular_total() for c in compras)
    total_productos = productos.count()
    total_stock = productos.aggregate(total_stock=Sum('stock'))['total_stock'] or 0
    valor_inventario = sum(p.stock * float(p.precio) for p in productos)

    contexto = {
        'tipo': tipo,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'total_ventas': total_ventas,
        'total_compras': total_compras,
        'total_productos': total_productos,
        'total_stock': total_stock,
        'valor_inventario': valor_inventario,
        'ventas': ventas,
        'compras': compras,
    }
    return render(request, 'reportes.html', contexto)

# ==================== EMPLEADO ====================

@login_required
@solo_empleado
@require_http_methods(["GET"])
def inventario_empleado(request):
    """Panel de control para empleados con acceso limitado."""
    from datetime import date
    productos_bajo_stock = Producto.objects.filter(stock__lte=F('stock_minimo')).count()
    total_productos = Producto.objects.count()
    total_ventas = Venta.objects.count()
    ventas_hoy = Venta.objects.filter(fecha_venta=date.today()).count()
    
    contexto = {
        'productos_bajo_stock': productos_bajo_stock,
        'total_productos': total_productos,
        'total_ventas': total_ventas,
        'ventas_hoy': ventas_hoy,
    }
    return render(request, 'empleado/inventario.html', contexto)

@login_required
@solo_empleado
@require_http_methods(["GET"])
def productos_empleado(request):
    """Vista para empleados: ver todos los productos (sin editar ni eliminar)."""
    query = request.GET.get('q', '').strip()
    productos = Producto.objects.all()
    if query:
        productos = productos.filter(
            Q(nombre_producto__icontains=query) |
            Q(codigo__icontains=query) |
            Q(descripcion__icontains=query)
        )
    contexto = {'productos': productos, 'query': query}
    return render(request, 'empleado/productos.html', contexto)

@login_required
@solo_empleado
@require_http_methods(["GET"])
def clientes_empleado(request):
    """Vista para empleados: ver todos los clientes (sin editar ni eliminar)."""
    query = request.GET.get('q', '').strip()
    clientes = Cliente.objects.all()
    if query:
        clientes = clientes.filter(
            Q(nombre__icontains=query) |
            Q(email__icontains=query) |
            Q(telefono__icontains=query)
        )
    contexto = {'clientes': clientes, 'query': query}
    return render(request, 'empleado/clientes.html', contexto)

@login_required
@solo_empleado
@require_http_methods(["GET"])
def proveedores_empleado(request):
    """Vista para empleados: ver todos los proveedores (sin editar ni eliminar)."""
    query = request.GET.get('q', '').strip()
    proveedores = Proveedor.objects.all()
    if query:
        proveedores = proveedores.filter(
            Q(nombre_proveedor__icontains=query) |
            Q(email__icontains=query) |
            Q(telefono__icontains=query)
        )
    contexto = {'proveedores': proveedores, 'query': query}
    return render(request, 'empleado/proveedores.html', contexto)

@login_required
@solo_empleado
@require_http_methods(["GET"])
def ventas_empleado(request):
    """Vista de ventas para empleados: ver todas las ventas."""
    ventas = Venta.objects.all().order_by('-fecha_venta')
    contexto = {'ventas': ventas}
    return render(request, 'empleado/ventas.html', contexto)

@login_required
@solo_empleado
@require_http_methods(["GET", "POST"])
def agregar_venta_empleado(request):
    """Permite a empleados crear una venta con detalles."""
    if request.method == 'POST':
        form = VentaForm(request.POST)
        formset = DetalleVentaFormSet(request.POST, queryset=DetalleVenta.objects.none())
        
        if form.is_valid():
            # Contar detalles válidos (con producto rellenado)
            valid_details = []
            for detail_form in formset:
                # Si el formulario es válido y tiene producto, es un detalle válido
                if detail_form.is_valid() and detail_form.cleaned_data.get('producto'):
                    valid_details.append(detail_form)
            
            if valid_details:
                with transaction.atomic():
                    venta = form.save(commit=False)
                    venta.usuario = request.user
                    venta.save()
                    
                    # Guardar detalles y actualizar stock
                    for detail_form in valid_details:
                        if not detail_form.cleaned_data.get('DELETE', False):
                            detalle = detail_form.save(commit=False)
                            detalle.venta = venta
                            detalle.save()
                            
                            # Actualizar stock del producto
                            producto = detalle.producto
                            producto.stock -= detalle.cantidad
                            producto.save()
                    
                    messages.success(request, 'Venta creada exitosamente.')
                    return redirect('ventas_empleado')
            else:
                messages.error(request, 'Debes agregar al menos un artículo a la venta.')
        else:
            if form.errors:
                for field, errors in form.errors.items():
                    messages.error(request, f'{field}: {errors[0]}')
    else:
        form = VentaForm()
        formset = DetalleVentaFormSet(queryset=DetalleVenta.objects.none())
    
    return render(request, 'empleado/agregar_venta.html', {'form': form, 'formset': formset})

@login_required
@solo_empleado
@require_http_methods(["GET", "POST"])
def editar_venta_empleado(request, id):
    """Permite a empleados editar una venta existente."""
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
                return redirect('ventas_empleado')
    else:
        form = VentaForm(instance=venta)
        formset = DetalleVentaFormSet(instance=venta)
    
    return render(request, 'empleado/editar_venta.html', {'form': form, 'formset': formset, 'venta': venta})

@login_required
@solo_empleado
@require_http_methods(["GET"])
def compras_empleado(request):
    """Vista de compras para empleados: ver todas las compras."""
    compras = Compra.objects.all().order_by('-fecha_compra')
    contexto = {'compras': compras}
    return render(request, 'empleado/compras.html', contexto)

@login_required
@solo_empleado
@require_http_methods(["GET", "POST"])
def agregar_compra_empleado(request):
    """Permite a empleados crear una compra con detalles."""
    if request.method == 'POST':
        form = CompraForm(request.POST)
        formset = DetalleCompraFormSet(request.POST, queryset=DetalleCompra.objects.none())
        
        if form.is_valid():
            # Contar detalles válidos (con producto rellenado)
            valid_details = []
            for detail_form in formset:
                # Si el formulario es válido y tiene producto, es un detalle válido
                if detail_form.is_valid() and detail_form.cleaned_data.get('producto'):
                    valid_details.append(detail_form)
            
            if valid_details:
                with transaction.atomic():
                    compra = form.save(commit=False)
                    compra.usuario = request.user
                    compra.save()
                    
                    # Guardar detalles y actualizar stock
                    for detail_form in valid_details:
                        if not detail_form.cleaned_data.get('DELETE', False):
                            detalle = detail_form.save(commit=False)
                            detalle.compra = compra
                            detalle.save()
                            
                            # Actualizar stock del producto
                            producto = detalle.producto
                            producto.stock += detalle.cantidad
                            producto.save()
                    
                    messages.success(request, 'Compra creada exitosamente.')
                    return redirect('compras_empleado')
            else:
                messages.error(request, 'Debes agregar al menos un artículo a la compra.')
        else:
            if form.errors:
                for field, errors in form.errors.items():
                    messages.error(request, f'{field}: {errors[0]}')
    else:
        form = CompraForm()
        formset = DetalleCompraFormSet(queryset=DetalleCompra.objects.none())
    
    return render(request, 'empleado/agregar_compra.html', {'form': form, 'formset': formset})

@login_required
@solo_empleado
@require_http_methods(["GET", "POST"])
def editar_compra_empleado(request, id):
    """Permite a empleados editar una compra existente."""
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
                return redirect('compras_empleado')
    else:
        form = CompraForm(instance=compra)
        formset = DetalleCompraFormSet(instance=compra)
    
    return render(request, 'empleado/editar_compra.html', {'form': form, 'formset': formset, 'compra': compra})

@login_required
@solo_empleado
@require_http_methods(["GET"])
def stock_critico(request):
    """Vista para empleados: ver productos con stock crítico."""
    from django.db.models import Q
    # Productos con stock crítico: stock <= 5 OR stock <= stock_mínimo
    productos = Producto.objects.filter(Q(stock__lte=5) | Q(stock__lte=F('stock_minimo')))
    return render(request, 'empleado/stock_critico.html', {'productos': productos})

# Prueba git

