// Sistema Global de Ayuda
const ayudaContenido = {
    'login': {
        titulo: 'Ayuda - Iniciar Sesión',
        contenido: `
            <h6>¿Cómo iniciar sesión?</h6>
            <p>Sigue estos pasos para acceder al sistema:</p>
            <ul class="mt-3">
                <li><strong>Usuario:</strong> Ingresa tu nombre de usuario o email.</li>
                <li><strong>Contraseña:</strong> Ingresa tu contraseña. Usa el ícono de ojo para verla.</li>
                <li><strong>Botón Ingresar:</strong> Haz clic para acceder al sistema.</li>
            </ul>
            <hr>
            <p class="text-muted small"><strong>¿Olvidaste tu contraseña?</strong> Contacta con el administrador para recuperarla.</p>
            <p class="text-muted small"><strong>Tip:</strong> Usa el botón de Ayuda (?) para obtener información en cualquier página.</p>
        `
    },
    'inicio': {
        titulo: 'Ayuda - Panel Principal',
        contenido: `
            <h6>Bienvenido al Panel Principal</h6>
            <p>Este es tu centro de control para acceder a todas las funciones del sistema.</p>
            <ul class="mt-3">
                <li><strong>Dashboard:</strong> Visualiza el resumen de tu operación.</li>
                <li><strong>Menú Lateral:</strong> Accede a todas las funciones del sistema.</li>
                <li><strong>Mi Perfil:</strong> Cambia tu contraseña desde el menú superior.</li>
            </ul>
            <hr>
            <p class="text-muted small"><strong>Tip:</strong> Puedes colapsar el menú lateral haciendo clic en el ícono de hamburguesa.</p>
        `
    },
    'clientes': {
        titulo: 'Ayuda - Gestión de Clientes',
        contenido: `
            <h6>Gestión de Clientes</h6>
            <p>Administra toda la información de tus clientes.</p>
            <ul class="mt-3">
                <li><strong>Agregar Cliente:</strong> Haz clic en "Agregar Cliente" e ingresa los datos.</li>
                <li><strong>Editar Cliente:</strong> Selecciona un cliente y modifica sus datos.</li>
                <li><strong>Eliminar Cliente:</strong> Elimina clientes que ya no necesites.</li>
                <li><strong>Ver Detalles:</strong> Haz clic en el nombre para ver información completa.</li>
            </ul>
            <hr>
            <p class="text-muted small"><strong>Nota:</strong> Asegúrate de ingresar el email y teléfono correctamente.</p>
        `
    },
    'productos': {
        titulo: 'Ayuda - Catálogo de Productos',
        contenido: `
            <h6>Catálogo de Productos</h6>
            <p>Administra todos los productos de tu inventario.</p>
            <ul class="mt-3">
                <li><strong>Agregar Producto:</strong> Crea nuevos productos con nombre, código y precio.</li>
                <li><strong>Editar Producto:</strong> Modifica precios, stocks y otros datos.</li>
                <li><strong>Ver Detalles:</strong> Consulta historial de movimientos por producto.</li>
                <li><strong>Buscar:</strong> Usa la búsqueda para encontrar productos rápidamente.</li>
            </ul>
            <hr>
            <p class="text-muted small"><strong>Tip:</strong> El código de producto debe ser único.</p>
        `
    },
    'proveedores': {
        titulo: 'Ayuda - Gestión de Proveedores',
        contenido: `
            <h6>Gestión de Proveedores</h6>
            <p>Administra información de tus proveedores.</p>
            <ul class="mt-3">
                <li><strong>Agregar Proveedor:</strong> Registra nuevos proveedores.</li>
                <li><strong>Editar Proveedor:</strong> Actualiza datos de contacto y detalles.</li>
                <li><strong>Eliminar Proveedor:</strong> Elimina proveedores inactivos.</li>
                <li><strong>Ver Compras:</strong> Consulta historial de compras por proveedor.</li>
            </ul>
            <hr>
            <p class="text-muted small"><strong>Importante:</strong> Mantén los datos de contacto actualizados.</p>
        `
    },
    'ventas': {
        titulo: 'Ayuda - Registro de Ventas',
        contenido: `
            <h6>Registro de Ventas</h6>
            <p>Registra y administra todas tus transacciones de venta.</p>
            <ul class="mt-3">
                <li><strong>Crear Venta:</strong> Selecciona cliente y productos, ingresa cantidades.</li>
                <li><strong>Editar Venta:</strong> Modifica detalles de ventas registradas.</li>
                <li><strong>Eliminar Venta:</strong> Cancela ventas si es necesario.</li>
                <li><strong>Ver Detalles:</strong> Consulta desglose de productos y totales.</li>
            </ul>
            <hr>
            <p class="text-muted small"><strong>Nota:</strong> El sistema actualiza automáticamente el inventario.</p>
        `
    },
    'compras': {
        titulo: 'Ayuda - Registro de Compras',
        contenido: `
            <h6>Registro de Compras</h6>
            <p>Administra tus compras a proveedores.</p>
            <ul class="mt-3">
                <li><strong>Crear Compra:</strong> Selecciona proveedor y productos.</li>
                <li><strong>Editar Compra:</strong> Modifica detalles de la compra.</li>
                <li><strong>Eliminar Compra:</strong> Cancela compras registradas.</li>
                <li><strong>Ver Historial:</strong> Consulta todas las compras realizadas.</li>
            </ul>
            <hr>
            <p class="text-muted small"><strong>Tip:</strong> Verifica el stock disponible antes de crear compras.</p>
        `
    },
    'inventario': {
        titulo: 'Ayuda - Consulta de Inventario',
        contenido: `
            <h6>Consulta de Inventario</h6>
            <p>Consulta el estado actual de tu inventario.</p>
            <ul class="mt-3">
                <li><strong>Buscar Producto:</strong> Encuentra productos por nombre o código.</li>
                <li><strong>Ver Stock:</strong> Consulta cantidad disponible.</li>
                <li><strong>Ver Precio:</strong> Información de precios de compra y venta.</li>
                <li><strong>Filtrar:</strong> Usa filtros para ver productos específicos.</li>
            </ul>
            <hr>
            <p class="text-muted small"><strong>Nota:</strong> Los datos se actualizan en tiempo real.</p>
        `
    },
    'movimientos': {
        titulo: 'Ayuda - Historial de Movimientos',
        contenido: `
            <h6>Historial de Movimientos</h6>
            <p>Consulta el historial completo de movimientos de inventario.</p>
            <ul class="mt-3">
                <li><strong>Filtrar por Tipo:</strong> Visualiza entradas o salidas.</li>
                <li><strong>Filtrar por Fecha:</strong> Consulta movimientos en un período específico.</li>
                <li><strong>Ver Detalles:</strong> Haz clic en un movimiento para más información.</li>
                <li><strong>Descargar:</strong> Exporta el historial si es necesario.</li>
            </ul>
            <hr>
            <p class="text-muted small"><strong>Tip:</strong> Usa los filtros para auditorías y reconciliaciones.</p>
        `
    },
    'reportes': {
        titulo: 'Ayuda - Reportes',
        contenido: `
            <h6>Reportes del Sistema</h6>
            <p>Genera reportes detallados de tu operación.</p>
            <ul class="mt-3">
                <li><strong>Reporte de Ventas:</strong> Análisis de ventas por período.</li>
                <li><strong>Reporte de Compras:</strong> Detalle de compras realizadas.</li>
                <li><strong>Inventario Crítico:</strong> Productos con stock bajo.</li>
                <li><strong>Descargar PDF:</strong> Descarga reportes en formato PDF.</li>
            </ul>
            <hr>
            <p class="text-muted small"><strong>Nota:</strong> Los reportes incluyen gráficos y análisis.</p>
        `
    },
    'usuarios': {
        titulo: 'Ayuda - Gestión de Usuarios',
        contenido: `
            <h6>Gestión de Usuarios</h6>
            <p>Administra los usuarios del sistema.</p>
            <ul class="mt-3">
                <li><strong>Agregar Usuario:</strong> Crea nuevas cuentas de usuario.</li>
                <li><strong>Editar Usuario:</strong> Modifica datos y roles.</li>
                <li><strong>Cambiar Contraseña:</strong> Establece nueva contraseña para usuarios.</li>
                <li><strong>Activar/Desactivar:</strong> Controla el acceso al sistema.</li>
                <li><strong>Asignar Rol:</strong> Define permisos: Administrador, Empleado o Invitado.</li>
            </ul>
            <hr>
            <p class="text-muted small"><strong>Importante:</strong> Solo administradores pueden gestionar usuarios.</p>
        `
    },
    'stock-critico': {
        titulo: 'Ayuda - Stock Crítico',
        contenido: `
            <h6>Stock Crítico</h6>
            <p>Gestiona productos con stock por debajo del mínimo.</p>
            <ul class="mt-3">
                <li><strong>Productos Bajos:</strong> Lista de artículos que necesitan reorden.</li>
                <li><strong>Cantidad Mínima:</strong> Nivel de stock configurado.</li>
                <li><strong>Crear Compra:</strong> Acceso rápido para crear órdenes de compra.</li>
                <li><strong>Alertas:</strong> Recibe notificaciones de productos críticos.</li>
            </ul>
            <hr>
            <p class="text-muted small"><strong>Tip:</strong> Revisa regularmente esta sección para evitar faltantes.</p>
        `
    },
    'cambiar-contrasena': {
        titulo: 'Ayuda - Cambiar Contraseña',
        contenido: `
            <h6>Cambiar Contraseña</h6>
            <p>Actualiza tu contraseña de acceso al sistema.</p>
            <ul class="mt-3">
                <li><strong>Contraseña Actual:</strong> Ingresa tu contraseña actual.</li>
                <li><strong>Nueva Contraseña:</strong> Define una contraseña segura.</li>
                <li><strong>Confirmar:</strong> Repite la nueva contraseña para confirmar.</li>
                <li><strong>Requisitos:</strong> La contraseña debe ser diferente a la anterior.</li>
            </ul>
            <hr>
            <p class="text-muted small"><strong>Seguridad:</strong> Elige una contraseña fuerte con letras, números y símbolos.</p>
        `
    },
    'default': {
        titulo: 'Ayuda del Sistema',
        contenido: `
            <h6>Bienvenido al Sistema de Gestión de Inventario</h6>
            <p>¿Cómo podemos ayudarte?</p>
            <ul class="mt-3">
                <li>Usa el menú lateral para navegar entre secciones.</li>
                <li>Cada sección tiene funciones específicas para gestionar inventario.</li>
                <li>Consulta la ayuda de cada página para más detalles.</li>
                <li>Cambio de contraseña disponible en el menú de usuario (esquina superior derecha).</li>
            </ul>
            <hr>
            <p class="text-muted small"><strong>Nota:</strong> Si necesitas ayuda adicional, contacta con el administrador.</p>
        `
    }
};

// Función para detectar la página actual
function detectarPaginaActual() {
    const pathname = window.location.pathname.toLowerCase();
    
    if (pathname.includes('/login/') || pathname.includes('/accounts/login/')) return 'login';
    if (pathname.includes('/usuarios/')) return 'usuarios';
    if (pathname.includes('/clientes/')) return 'clientes';
    if (pathname.includes('/productos/')) return 'productos';
    if (pathname.includes('/proveedores/')) return 'proveedores';
    if (pathname.includes('/ventas/')) return 'ventas';
    if (pathname.includes('/compras/')) return 'compras';
    if (pathname.includes('/inventario/')) return 'inventario';
    if (pathname.includes('/movimientos/')) return 'movimientos';
    if (pathname.includes('/reportes/')) return 'reportes';
    if (pathname.includes('/stock-critico/')) return 'stock-critico';
    if (pathname.includes('/password-change/') || pathname.includes('/cambiar-contrasena/')) return 'cambiar-contrasena';
    if (pathname.includes('/inicio/') || pathname === '/') return 'inicio';
    
    return 'default';
}

// Función para mostrar el modal de ayuda
function mostrarAyuda() {
    const paginaActual = detectarPaginaActual();
    const ayuda = ayudaContenido[paginaActual] || ayudaContenido['default'];
    
    const modalTitle = document.querySelector('#ayudaModal .modal-title');
    const modalBody = document.querySelector('#ayudaModal .modal-body');
    
    if (modalTitle) modalTitle.textContent = ayuda.titulo;
    if (modalBody) modalBody.innerHTML = ayuda.contenido;
    
    const modalElement = new bootstrap.Modal(document.getElementById('ayudaModal'));
    modalElement.show();
}

// Inicializar evento del botón de ayuda
document.addEventListener('DOMContentLoaded', function() {
    const btnAyuda = document.getElementById('btnAyuda');
    if (btnAyuda) {
        btnAyuda.addEventListener('click', mostrarAyuda);
    }
});
