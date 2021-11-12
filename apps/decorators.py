from django.http import HttpResponse
from django.shortcuts import redirect

def usuarioNoLogeado(view_func):
    def envoltFunc(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('index')
        else:
            return view_func(request, *args, **kwargs)

    return envoltFunc

def usuarioPermitido(allowed_roles = []):
    def decorator(view_func):
        def envoltFunc(request, *args, **kwargs):

            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allowed_roles:
               return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('No cuentas con los permisos para acceder a este sitio')
        return envoltFunc
    return decorator


def admin_view(view_func):
    def decorator(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name

        if group == 'Admin':
            return view_func(request, *args, **kwargs)
            
        if group == 'Bodega':
            return redirect('index_bodeguero')

        if group == 'Cajero':
            return redirect('index_cajero')

        if group == 'Cocinero':
            return redirect('index_cocina')

        if group == 'Garzon':
            return redirect('main_garzon')
    return decorator