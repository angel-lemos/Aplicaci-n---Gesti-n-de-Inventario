from django.urls import path
from . import views

urlpatterns = [
    # INICIO
    path('', views.inicio, name='inicio'),
    
    #LOGOUT
    path('logout/', views.logout_view, name='logout'),
    
    # CLIENTES
    path('clientes/', views.ver_clientes, name='ver_clientes'),
    path('clientes/agregar/', views.agregar_cliente, name='agregar_cliente'),
    path('clientes/editar/<int:id>/', views.editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:id>/', views.eliminar_cliente, name='eliminar_cliente'),
    
    # USUARIOS
    path('usuarios/', views.ver_usuarios, name='ver_usuarios'),
    path('usuarios/agregar/', views.agregar_usuario, name='agregar_usuario'),
    path('usuarios/activar/<int:id>/', views.activar_usuario, name='activar_usuario'),
    path('usuarios/eliminar/<int:id>/', views.eliminar_usuario, name='eliminar_usuario'),
    
    # PROVEEDORES
    path('proveedores/', views.ver_proveedores, name='ver_proveedores'),
    path('proveedores/agregar/', views.agregar_proveedor, name='agregar_proveedor'),
    path('proveedores/editar/<int:id>/', views.editar_proveedor, name='editar_proveedor'),
    path('proveedores/eliminar/<int:id>/', views.eliminar_proveedor, name='eliminar_proveedor'),
    
    # PRODUCTOS
    path('productos/', views.ver_productos, name='ver_productos'),
    path('productos/agregar/', views.agregar_producto, name='agregar_producto'),
    path('productos/editar/<int:id>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:id>/', views.eliminar_producto, name='eliminar_producto'),
    path('inventario/', views.ver_inventario, name='consultar_inventario'),
    path('inventario/producto/<int:id>/', views.detalle_producto, name='detalle_producto'),
    path('movimientos/', views.ver_movimientos, name='ver_movimientos'),
    path('reportes/', views.ver_reportes, name='ver_reportes'),
    
    # VENTAS
    path('ventas/', views.ver_ventas, name='ver_ventas'),
    path('ventas/agregar/', views.agregar_venta, name='agregar_venta'),
    path('ventas/editar/<int:id>/', views.editar_venta, name='editar_venta'),
    path('ventas/eliminar/<int:id>/', views.eliminar_venta, name='eliminar_venta'),
    
    # COMPRAS
    path('compras/', views.ver_compras, name='ver_compras'),
    path('compras/agregar/', views.agregar_compra, name='agregar_compra'),
    path('compras/editar/<int:id>/', views.editar_compra, name='editar_compra'),
    path('compras/eliminar/<int:id>/', views.eliminar_compra, name='eliminar_compra'),
    
    # EMPLEADO - Vistas limitadas
    path('empleado/inventario/', views.inventario_empleado, name='inventario_empleado'),
    path('empleado/productos/', views.productos_empleado, name='productos_empleado'),
    path('empleado/clientes/', views.clientes_empleado, name='clientes_empleado'),
    path('empleado/proveedores/', views.proveedores_empleado, name='proveedores_empleado'),
    path('empleado/ventas/', views.ventas_empleado, name='ventas_empleado'),
    path('empleado/ventas/agregar/', views.agregar_venta_empleado, name='agregar_venta_empleado'),
    path('empleado/ventas/editar/<int:id>/', views.editar_venta_empleado, name='editar_venta_empleado'),
    path('empleado/compras/', views.compras_empleado, name='compras_empleado'),
    path('empleado/compras/agregar/', views.agregar_compra_empleado, name='agregar_compra_empleado'),
    path('empleado/compras/editar/<int:id>/', views.editar_compra_empleado, name='editar_compra_empleado'),
    path('empleado/stock-critico/', views.stock_critico, name='stock_critico'),
]
