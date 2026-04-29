# 📦 Sistema de Gestión de Inventario

Una aplicación web completa y profesional para la gestión integral de inventario, ventas, compras y clientes desarrollada con **Django 6.0.3** y **Bootstrap 5.3.0**.

## 🎯 Descripción General

Este sistema está diseñado para empresas y comercios que necesitan gestionar su inventario de forma eficiente y profesional. Permite controlar el stock de productos, registrar ventas y compras, administrar clientes y proveedores, generar reportes y mucho más.

## ✨ Características Principales

### 👥 Gestión de Usuarios
- ✅ Sistema de autenticación seguro
- ✅ Roles: Superadministrador, Administrador, Empleado, Invitado
- ✅ Control de acceso basado en roles
- ✅ Cambio de contraseña con íconos de visualización
- ✅ Gestión de usuarios por administrador
- ✅ Activación/desactivación de usuarios

### 📦 Gestión de Productos
- ✅ Crear, editar, eliminar productos
- ✅ Consulta de stock en tiempo real
- ✅ Búsqueda avanzada de productos
- ✅ Información detallada por producto
- ✅ Historial de movimientos por producto

### 🛒 Gestión de Ventas
- ✅ Registro de ventas con cliente y productos
- ✅ Actualización automática de inventario
- ✅ Edición y eliminación de ventas
- ✅ Historial completo de transacciones
- ✅ Cálculo automático de totales

### 📥 Gestión de Compras
- ✅ Registro de compras a proveedores
- ✅ Selección de productos y cantidades
- ✅ Actualización de stock al registrar compra
- ✅ Edición y eliminación de compras
- ✅ Seguimiento de gastos

### 👨‍💼 Gestión de Clientes
- ✅ CRUD completo de clientes
- ✅ Información de contacto
- ✅ Historial de compras por cliente
- ✅ Búsqueda rápida

### 🚚 Gestión de Proveedores
- ✅ Administración de proveedores
- ✅ Datos de contacto
- ✅ Historial de compras
- ✅ Información de términos de compra

### 📊 Reportes y Análisis
- ✅ Reporte de ventas
- ✅ Reporte de compras
- ✅ Consulta de inventario
- ✅ Historial de movimientos
- ✅ Alertas de stock crítico
- ✅ Exportación a PDF

### 🔒 Seguridad
- ✅ Sesiones que cierran al cerrar el navegador
- ✅ Protección CSRF
- ✅ Autenticación de dos niveles
- ✅ Permisos granulares por rol
- ✅ Contraseñas encriptadas

### ❓ Ayuda y Usabilidad
- ✅ Sistema de ayuda contextual por página
- ✅ Botón de ayuda en todas las páginas
- ✅ Iconos intuitivos de Bootstrap Icons
- ✅ Interfaz responsiva y amigable

## 🚀 Instalación

### Requisitos Previos
- Python 3.8+
- pip (gestor de paquetes de Python)
- Virtual Environment (recomendado)

### Pasos de Instalación

1. **Clonar el repositorio**
   ```bash
   git clone <url-del-repositorio>
   cd Aplicaci-n---Gesti-n-de-Inventario
   ```

2. **Crear y activar el ambiente virtual**
   
   En Windows (PowerShell):
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
   
   En Linux/Mac:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Realizar migraciones de base de datos**
   ```bash
   python manage.py migrate
   ```

5. **Crear superusuario (administrador)**
   ```bash
   python manage.py createsuperuser
   ```
   Sigue las instrucciones para crear tu usuario administrador.

6. **Ejecutar el servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```
   La aplicación estará disponible en: `http://127.0.0.1:8000`

## 📖 Cómo Usar

### 1. Iniciar Sesión
- Accede a `http://127.0.0.1:8000` en tu navegador
- Ingresa tu usuario y contraseña
- Usa el botón de "Ayuda" para obtener información de login

### 2. Panel Principal
- Visualiza el resumen de tu operación
- Accede a todas las funciones desde el menú lateral
- Cambia tu contraseña desde el menú de usuario (esquina superior derecha)

### 3. Gestión de Productos
- Ve a **Productos** en el menú lateral
- Haz clic en "Agregar Producto" para crear un nuevo producto
- Edita o elimina productos existentes
- Visualiza el stock y detalles de cada producto

### 4. Registro de Ventas
- Ve a **Ventas**
- Haz clic en "Agregar Venta"
- Selecciona cliente y productos
- Ingresa cantidades y guarda
- El inventario se actualiza automáticamente

### 5. Registro de Compras
- Ve a **Compras**
- Haz clic en "Agregar Compra"
- Selecciona proveedor y productos
- Confirma la compra
- El stock se incrementa automáticamente

### 6. Consulta de Inventario
- Ve a **Inventario**
- Busca productos por nombre o código
- Visualiza stock disponible y precios
- Usa filtros para búsquedas específicas

### 7. Cambiar Contraseña
- Haz clic en tu usuario (esquina superior derecha)
- Selecciona "Cambiar contraseña"
- Ingresa contraseña actual y nueva contraseña
- Usa el ícono de ojo para ver/ocultar contraseña

### 8. Ver Ayuda
- Haz clic en el ícono de "?" (signo de interrogación)
- Obtén información contextual de la página actual
- La ayuda se adapta automáticamente a cada sección

## 🏗️ Estructura del Proyecto

```
Aplicación---Gestión-de-Inventario/
│
├── Gestion_inventario/          # Configuración principal de Django
│   ├── settings.py              # Configuración del proyecto
│   ├── urls.py                  # URLs principales
│   ├── wsgi.py                  # Configuración WSGI
│   └── asgi.py                  # Configuración ASGI
│
├── inventario/                  # Aplicación principal
│   ├── models.py                # Modelos de base de datos
│   ├── views.py                 # Vistas y lógica de negocio
│   ├── forms.py                 # Formularios
│   ├── urls.py                  # URLs de la aplicación
│   ├── admin.py                 # Administración
│   ├── migrations/              # Migraciones de BD
│   ├── templates/               # Plantillas HTML
│   ├── static/
│   │   └── js/
│   │       └── ayuda.js         # Sistema de ayuda contextual
│   └── decorators.py            # Decoradores personalizados
│
├── manage.py                    # Utilidad de gestión de Django
├── requirements.txt             # Dependencias del proyecto
├── db.sqlite3                   # Base de datos SQLite
├── README.md                    # Este archivo
└── .venv/                       # Ambiente virtual (no incluido en git)
```

## 🗄️ Modelos de Base de Datos

### Usuario (Django User)
- Nombre de usuario
- Email
- Contraseña encriptada
- Estado (activo/inactivo)

### Perfil
- Relación 1-1 con Usuario
- Rol (Administrador, Empleado, Invitado, SuperAdmin)

### Producto
- Nombre
- Código
- Descripción
- Precio de compra
- Precio de venta
- Stock actual
- Stock mínimo

### Cliente
- Nombre
- Email
- Teléfono
- Dirección
- Ciudad

### Proveedor
- Nombre
- Email
- Teléfono
- Dirección

### Venta
- Cliente
- Fecha
- Productos (relación muchos-a-muchos)
- Cantidades
- Total

### Compra
- Proveedor
- Fecha
- Productos
- Cantidades
- Total

## 🔐 Roles y Permisos

### Superadministrador
- Acceso completo a todas las funciones
- Gestión de usuarios
- Cambio de contraseña de cualquier usuario
- Acceso a todos los reportes

### Administrador
- Gestión de productos, clientes, proveedores
- Registro de ventas y compras
- Visualización de reportes
- Cambio de contraseña solo de empleados e invitados
- Gestión limitada de usuarios

### Empleado
- Registro de ventas
- Consulta de inventario
- Visualización de datos
- Cambio de su propia contraseña

### Invitado
- Solo lectura
- Consulta de inventario
- Visualización de reportes sin edición
- Cambio de su propia contraseña

## 🛠️ Configuración Avanzada

### Variables de Entorno (opcional)
Puedes crear un archivo `.env` para configuraciones sensibles:

```
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

### Configuración de Email (para futuras mejoras)
En `settings.py`:
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu-email@gmail.com'
EMAIL_HOST_PASSWORD = 'tu-contraseña'
```

### Base de Datos en Producción
Para producción, se recomienda usar PostgreSQL:
```bash
pip install psycopg2-binary
```

## 📚 Dependencias Principales

- **Django 6.0.3**: Framework web
- **Bootstrap 5.3.0**: Framework CSS
- **Bootstrap Icons**: Iconos
- **reportlab**: Generación de PDF
- **django-widget-tweaks**: Manipulación de widgets
- **python-dateutil**: Utilities de fechas

Ver `requirements.txt` para la lista completa.

## 🐛 Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'django'"
**Solución:** Activa el ambiente virtual
```bash
.venv\Scripts\Activate.ps1  # Windows PowerShell
source .venv/bin/activate    # Linux/Mac
```

### Error: "CSRF token incorrect"
**Solución:** Limpia las cookies del navegador y recarga la página.

### Error: "Base de datos bloqueada"
**Solución:** Cierra todos los procesos de Django y borra `db.sqlite3`, luego ejecuta:
```bash
python manage.py migrate
```

### Botón de ver contraseña no funciona
**Solución:** Limpia la caché del navegador (Ctrl+Shift+Supr) y recarga.

## 📞 Soporte y Contacto

Para reportar bugs o sugerir mejoras:
1. Consulta la sección **Ayuda** en cualquier página de la aplicación
2. Contacta al equipo de desarrollo

## 📄 Licencia

Este proyecto está disponible bajo licencia privada. Todos los derechos reservados.

## 👥 Equipo de Desarrollo

**Sistema de Gestión de Inventario**
- Desarrollo y diseño completo
- Soporte técnico
- Mejoras continuas

## 🎉 Características Especiales

### Sistema de Ayuda Inteligente
- Detecta automáticamente la página actual
- Proporciona ayuda contextual relevante
- Un único archivo JavaScript eficiente
- Sin ocupar espacio adicional

### Visualización de Contraseña
- Iconos de ojo para mostrar/ocultar
- Funciona en login, cambio de contraseña y cambio de contraseña de usuario
- Interfaz intuitiva y segura

### Interfaz Responsiva
- Compatible con desktop, tablet y móvil
- Menú colapsible en dispositivos pequeños
- Diseño moderno con Bootstrap 5

### Sesiones Seguras
- Cierran automáticamente al cerrar el navegador
- Protección CSRF habilitada
- Autenticación de dos niveles

## 🚀 Próximas Versiones

- Notificaciones por email
- Dashboard con gráficos interactivos
- Código de barras y QR
- Aplicación móvil
- API REST para integraciones
- Y muchas más...

## ✅ Testing

Para ejecutar pruebas unitarias:
```bash
python manage.py test
```

## 📦 Deployment en Producción

### Con Gunicorn
```bash
pip install gunicorn
gunicorn Gestion_inventario.wsgi:application --bind 0.0.0.0:8000
```

### Con Nginx (recomendado)
Consulta la documentación de Django para configuración completa de Nginx + Gunicorn.

---

**Última actualización:** 28 de abril de 2026
**Versión:** 1.0.0
**Estado:** En desarrollo activo ✅

¡Gracias por usar nuestro Sistema de Gestión de Inventario! 📦
