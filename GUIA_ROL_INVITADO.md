# Guía: Rol de Invitado en Gestión de Inventario

## Descripción
Se ha agregado un nuevo rol "Invitado" al sistema de gestión de inventario. Los usuarios con este rol tienen acceso de solo lectura a:
- **Consulta de Inventario**: Ver productos disponibles y su estado
- **Movimientos**: Historial de entradas y salidas de inventario
- **Reportes**: Análisis generales del sistema (inventario, ventas y compras)

## Características del Rol Invitado

### ✓ Permisos
- Ver inventario con búsqueda
- Consultar historial de movimientos (compras y ventas)
- Acceder a reportes generales
- Filtrar datos por fechas
- Ver información de clientes, proveedores y productos

### ✗ Restricciones
- No puede crear, editar ni eliminar productos
- No puede registrar ventas o compras
- No puede gestionar usuarios
- Solo lectura en todas las operaciones

## Instalación y Setup

### 1. Hacer Migraciones (si es necesario)
```bash
python manage.py migrate
```

### 2. Crear Usuario Invitado
Ejecutar el script de setup:
```bash
python setup_invitado.py
```

El script te pedirá una contraseña para el usuario. Esto creará:
- **Username**: `invitado`
- **Email**: `invitado@gestioninventario.local`
- **Rol**: Invitado
- **Estado**: Activo

### 3. Rutas Disponibles

Las siguientes rutas están disponibles para el rol invitado:

| Ruta | Descripción |
|------|-------------|
| `/invitado/inicio/` | Panel de inicio con estadísticas generales |
| `/invitado/inventario/` | Consulta de inventario con búsqueda |
| `/invitado/movimientos/` | Historial de movimientos de inventario |
| `/invitado/reportes/` | Reportes generales del sistema |

## Uso

### Acceso a las Vistas

1. **Panel de Inicio** (`/invitado/inicio/`)
   - Muestra estadísticas generales
   - Accesos rápidos a las principales funciones
   - Resumen de productos, clientes y proveedores

2. **Consultar Inventario** (`/invitado/inventario/`)
   - Buscar productos por nombre, código o descripción
   - Ver stock actual y precios
   - Identificar productos con stock bajo (en rojo/naranja)

3. **Ver Movimientos** (`/invitado/movimientos/`)
   - Filtrar por tipo (Entradas/Salidas)
   - Filtrar por rango de fechas
   - Ver detalles de compras y ventas
   - Información del usuario que realizó el movimiento

4. **Ver Reportes** (`/invitado/reportes/`)
   - **Reporte de Inventario**: Total de productos, stock total, valor estimado
   - **Reporte de Ventas**: Total de ventas registradas, monto total vendido
   - **Reporte de Compras**: Total de compras, monto total comprado

## Modificación del Rol

Si necesitas:

### Cambiar la Contraseña del Usuario Invitado
```bash
python manage.py changepassword invitado
```

### Desactivar/Reactivar el Usuario
En Django Admin o mediante código:
```python
from django.contrib.auth.models import User
usuario = User.objects.get(username='invitado')
usuario.is_active = False  # Desactivar
usuario.save()
```

### Cambiar Permisos
Para modificar los permisos, edita la función en `views.py`:
- `inicio_invitado`: Panel de inicio
- `inventario_invitado`: Consulta de inventario
- `movimientos_invitado`: Historial de movimientos
- `reportes_invitado`: Reportes generales

## Seguridad

- El rol invitado solo tiene acceso de lectura
- Los datos filtrados pueden modificarse según necesidades
- Se recomienda usar credenciales fuertes para la cuenta
- Monitorea el acceso del usuario invitado regularmente

## Archivos Modificados

- ✓ `inventario/models.py` - Agregado rol 'invitado' en ROLES
- ✓ `inventario/decorators.py` - Agregado decorador `solo_invitado()`
- ✓ `inventario/views.py` - Agregadas vistas para invitado
- ✓ `inventario/urls.py` - Agregadas rutas para invitado
- ✓ `inventario/templates/invitado/` - Nuevos templates
- ✓ `inventario/templatetags/` - Filtro personalizado `mul`
- ✓ `setup_invitado.py` - Script de creación de usuario

## Soporte

Si tienes problemas:
1. Verifica que las migraciones se hayan ejecutado
2. Confirma que el usuario 'invitado' existe: `User.objects.filter(username='invitado').exists()`
3. Revisa los logs de Django para errores
4. Verifica que los templates están en `inventario/templates/invitado/`
