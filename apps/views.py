from django.shortcuts import render, redirect, get_object_or_404
from .models import Reserva, Mesa, Plato, AuthUser
from datetime import datetime, timedelta
import base64
from .forms import ReservaForm, DatosReservaForm, MesaForm, datosAgregarMesaForm, CustomUserCreationFrom
from django.contrib.auth import authenticate, login
from django.contrib.messages import success
from django.contrib import messages
from django.db.models import Q, query, query_utils
from django.contrib.auth.decorators import login_required
# Create your views here.
from .decorators import usuarioPermitido, usuarioNoLogeado

#HTML GENERAL
def index(request):
    return render (request,'html/general/index.html')

def login_usuario(request):
    return render (request, 'registration/login.html')

def registro(request):
    data = {

        'form' : CustomUserCreationFrom()
    }
    if request.method == 'POST':
        formulario = CustomUserCreationFrom(data=request.POST)
        if  formulario.is_valid():
            formulario.save()
            user= authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            messages.success(request,'registro correctamente')
            return redirect(to='index')
        data["form"]= formulario

    return render (request, 'registration/registro.html', data)

def loginAsociado(request):
    return render (request, 'html/general/loginAsociado.html')

#HTML ADMIN
#@login_required(login_url = 'loginAsociado')
def admin_reportes(request):
    return render (request, 'html/admin/admin_reportes.html')

#@login_required(login_url = 'loginAsociado')
def agregar_usuario(request):
    return render (request, 'html/admin/agregar_usuario.html')

#@login_required(login_url = 'loginAsociado')
def gestion_solicitudes(request):
    return render (request, 'html/admin/gestion_solicitudes.html')

#@login_required(login_url = 'loginAsociado')
def gestion_usuario(request):
    usuarios = AuthUser.objects.all()

    queryset = request.GET.get("inputBuscarUsuario")
    if queryset:
        usuarios = AuthUser.objects.filter(
            Q(username__icontains = queryset) |
            Q(first_name__icontains = queryset) | 
            Q(last_name__icontains = queryset) |
            Q(email__icontains = queryset) 
        ).distinct()
    else:
        usuarios = AuthUser.objects.all()
    return render (request, 'html/admin/gestion_usuario.html', {'usuarios':usuarios})

#@login_required(login_url = 'loginAsociado')
def gestionMesas(request):
    mesas = Mesa.objects.all()

    queryset = request.GET.get("inputBuscarMesa")
    if queryset:
        mesas = Mesa.objects.filter(
            Q(id_mesa__icontains = queryset)
        ).distinct()
    else:
        mesas = Mesa.objects.all()
    return render (request, 'html/admin/gestionMesas.html', {'mesas':mesas})

#@login_required(login_url = 'loginAsociado')
#@usuarioPermitido(allowed_roles = ['admin'])
def index_admin(request):
    return render (request, 'html/admin/index_admin.html')

#@login_required(login_url = 'loginAsociado')
def modificar_usuario(request):
    return render (request, 'html/admin/modificar_usuario.html')

#@login_required(login_url = 'loginAsociado')
def solicitud_stock_proveedores(request):
    return render (request, 'html/admin/solicitud_stock_proveedores.html')

#@login_required(login_url = 'loginAsociado')
def solicitudes_enviadas(request):
    return render (request, 'html/admin/solicitudes_enviadas.html')

#@login_required(login_url = 'loginAsociado')
def solicitudes_recibidas(request):
    return render (request, 'html/admin/solicitudes_recibidas.html')

#@login_required(login_url = 'loginAsociado')
def ver_reservas(request):
    reservas = Reserva.objects.all()

    queryset = request.GET.get("inputBuscarReserva")
    if queryset:
        reservas = Reserva.objects.filter(
            Q(id_reserva__icontains = queryset) |
            Q(comentario__icontains = queryset)
        ).distinct()
    else:
        reservas = Reserva.objects.all()
    return render (request, 'html/admin/ver_reservas.html', {'reservas':reservas})

#@login_required(login_url = 'loginAsociado')
def agregar_mesa(request):
    if request.method == 'POST':

        datosAgregarMesa = datosAgregarMesaForm(request.POST)
        print(datosAgregarMesa)
        if datosAgregarMesa.is_valid():
            #Limpiar los datos del POST
            numMesaAgg = datosAgregarMesa.cleaned_data['numMesaAgg']
            dispMesaAgg = datosAgregarMesa.cleaned_data['dispMesaAgg']

            #Asignando variables para guardar
            try:
                ult_id = Mesa.objects.latest('id_mesa').id_mesa #Último ID registrado en reservas
            except:
                ult_id= 0
            id_mesav2 = int(str(ult_id)) + 1
            agg_mesa = Mesa(id_mesav2, numMesaAgg, dispMesaAgg)
            agg_mesa.save()
    else:
            aggMesaForm = MesaForm()
    return render (request, 'html/admin/agregar_mesa.html')


#HTML BODEGA
def gestion_bodega(request):
    return render (request, 'html/bodega/gestion_bodega.html')

#@login_required(login_url = 'loginAsociado')
def registro_bodega(request):
    return render (request, 'html/bodega/registro_bodega.html')


#HTML CLIENTE
def cliente_hacer_pedido(request):
    platos = Plato.objects.all()

    arreglo = []

    for i in platos:
        data = {
            'id_plato': i.id_plato,
            'nombre_plato': i.nombre_plato,
            'precio': i.precio,
            'tipo_plato': i.tipo_plato,
            'foto_plato': str(base64.b64encode(i.foto_plato.read()),'utf-8')
        }
        arreglo.append(data)

    return render (request, 'html/cliente/cliente_hacer_pedido.html', {'arreglo' :arreglo})#data)

def cliente_hacer_reserva(request):
    if request.method == 'POST':

        datos_reserva = DatosReservaForm(request.POST)

        if datos_reserva.is_valid():
            #Limpiar los datos del POST
            cantidad_personas = datos_reserva.cleaned_data['cantidad_personas']
            fecha_reserva = datos_reserva.cleaned_data['fecha'].strftime("%Y-%m-%d")
            hora_reserva = datos_reserva.cleaned_data['hora']
            comentario = datos_reserva.cleaned_data['comentario']

            #Asignando variables para guardar
            #Tengo que hacer el que pasaria si no hay registros para el id
            try:
                ultimo_id = Reserva.objects.latest('id_reserva').id_reserva #Último ID registrado en reservas
            except:
                ultimo_id= 0
            nuevo_id = int(str(ultimo_id)) + 1 #Se le suma 1
            fecha = str(fecha_reserva) + ' ' + str(hora_reserva)
            fecha_vence = datetime.strptime(fecha ,"%Y-%m-%d %H:%M") + timedelta(minutes=20)
            print(fecha_vence)
            reserva = Reserva(nuevo_id, cantidad_personas, fecha, comentario, fecha_vence)
            reserva.save()
    else:
        reserva_form = ReservaForm()
    return render (request, 'html/cliente/cliente_hacer_reserva.html')

def cliente_index(request):
    return render (request, 'html/cliente/cliente_index.html')

def Cliente_Observar_Disponibilidad(request):
    return render (request, 'html/cliente/Cliente_Observar_Disponibilidad.html')

def cliente_ver_reserva(request):
    reservas = Reserva.objects.all()
    return render (request, 'html/cliente/cliente_ver_reserva.html', {'reservas':reservas})

def eliminar_reservaAdm(request, id_reserva):
    reserva = get_object_or_404(Reserva, id = id_reserva)
    reserva.delete()
    return redirect(to = "ver_reservas")

#ENVIAR CORREO
def sendemail(email):
    pass

#Formularios
#Formulario de Hacer Reserva
#def crearReserva(request):
    