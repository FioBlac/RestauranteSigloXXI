from django.shortcuts import render

# Create your views here.


#HTML GENERAL
def index(request):
    return render (request,'index.html')

def login(request):
    return render (request, 'html/general/login.html')

def registro(request):
    return render (request, 'html/general/registro.html')

def loginAsociado(request):
    return render (request, 'html/general/loginAsociado.html')

def indexLogin(request):
    return render (request, 'html/general/indexLogin.html')


#HTML ADMIN
def admin_reportes(request):
    return render (request, 'html/admin/admin_reportes.html')

def agregar_usuario(request):
    return render (request, 'html/admin/agregar_usuario.html')

def gestion_solicitudes(request):
    return render (request, 'html/admin/gestion_solicitudes.html')

def gestion_usuario(request):
    return render (request, 'html/admin/gestion_usuario.html')

def gestionMesas(request):
    return render (request, 'html/admin/gestionMesas.html')

def index_admin(request):
    return render (request, 'html/admin/index_admin.html')

def modificar_usuario(request):
    return render (request, 'html/admin/modificar_usuario.html')

def solicitud_stock_proveedores(request):
    return render (request, 'html/admin/solicitud_stock_proveedores.html')

def solicitudes_enviadas(request):
    return render (request, 'html/admin/solicitudes_enviadas.html')

def solicitudes_recibidas(request):
    return render (request, 'html/admin/solicitudes_recibidas.html')

def ver_reservas(request):
    return render (request, 'html/admin/ver_reservas.html')


#HTML BODEGA
def gestion_bodega(request):
    return render (request, 'html/bodega/gestion_bodega.html')

def registro_bodega(request):
    return render (request, 'html/bodega/registro_bodega.html')


#HTML CLIENTE
def cliente_hacer_pedido(request):
    return render (request, 'html/cliente/cliente_hacer_pedido.html')

def cliente_hacer_reserva(request):
    return render (request, 'html/cliente/cliente_hacer_reserva.html')

def cliente_index(request):
    return render (request, 'html/cliente/cliente_index.html')

def Cliente_Observar_Disponibilidad(request):
    return render (request, 'html/cliente/Cliente_Observar_Disponibilidad.html')

def cliente_ver_reserva(request):
    return render (request, 'html/cliente/cliente_ver_reserva.html')
