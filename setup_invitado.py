"""
Script para crear el usuario 'invitado' con rol de invitado.
Ejecutar desde la raíz del proyecto: python setup_invitado.py
"""

import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(__file__))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Gestion_inventario.settings')
django.setup()

from django.contrib.auth.models import User
from inventario.models import Perfil

def crear_usuario_invitado():
    """Crea el usuario invitado si no existe."""
    
    try:
        # Verificar si el usuario ya existe
        usuario_existente = User.objects.filter(username='invitado').exists()
        
        if usuario_existente:
            usuario = User.objects.get(username='invitado')
            print(f"✓ El usuario 'invitado' ya existe")
            
            # Verificar el rol
            if hasattr(usuario, 'perfil'):
                print(f"✓ Rol actual: {usuario.perfil.get_rol_display()}")
            
            # Preguntar si desea actualizar la contraseña
            actualizar = input("\n¿Desea actualizar la contraseña del usuario? (s/n): ").lower()
            if actualizar == 's':
                nueva_contraseña = input("Ingrese la nueva contraseña: ")
                usuario.set_password(nueva_contraseña)
                usuario.save()
                print("✓ Contraseña actualizada exitosamente")
        else:
            # Crear el usuario
            contraseña = input("Ingrese la contraseña para el usuario 'invitado': ")
            
            usuario = User.objects.create_user(
                username='invitado',
                email='invitado@gestioninventario.local',
                password=contraseña,
                first_name='Usuario',
                last_name='Invitado',
                is_active=True,
                is_staff=False,
                is_superuser=False
            )
            
            # Crear el perfil con rol invitado
            Perfil.objects.filter(user=usuario).delete()  # Por si existe
            perfil = Perfil.objects.create(
                user=usuario,
                rol='invitado',
                telefono='-'
            )
            
            print("\n✓ Usuario 'invitado' creado exitosamente")
            print(f"  - Username: invitado")
            print(f"  - Email: invitado@gestioninventario.local")
            print(f"  - Rol: {perfil.get_rol_display()}")
            print(f"  - Estado: Activo")
        
        print("\n✓ Configuración completada")
        
    except Exception as e:
        print(f"✗ Error al crear el usuario: {str(e)}")
        return False
    
    return True

if __name__ == '__main__':
    print("=" * 50)
    print("Configuración del Usuario Invitado")
    print("=" * 50)
    crear_usuario_invitado()
