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
            if request.user.group.exists():
                group = request.user.group.all()[0].name

            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
                return HttpResponse('No cuentas con los permisos para acceder a este sitio')
        return envoltFunc
    return decorator