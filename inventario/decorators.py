from django.shortcuts import redirect
from django.contrib.auth.decorators import  login_required
from django.core.exceptions import PermissionDenied
from functools import wraps

def solo_empleado(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('login')

        perfil = getattr(request.user, 'perfil', None)

        if perfil and perfil.rol in ['empleado', 'administrador']:
            return view_func(request, *args, **kwargs)

        raise PermissionDenied

    return wrapper

def roles_permitidos(*roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                return redirect('login')

            if hasattr(request.user, 'perfil'):
                if request.user.perfil.rol in roles:
                    return view_func(request, *args, **kwargs)

            raise PermissionDenied

        return wrapper
    return decorator

def solo_invitado(view_func):
    """Decorador para permitir solo al rol invitado."""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if hasattr(request.user, 'perfil'):
            if request.user.perfil.rol == 'invitado':
                return view_func(request, *args, **kwargs)

        raise PermissionDenied

    return wrapper