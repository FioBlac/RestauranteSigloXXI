from django.shortcuts import render
from .forms import ReservaForm, DatosReservaForm, MesaForm, datosAgregarMesaForm
from .models import Reserva, Mesa, Plato
from datetime import datetime, timedelta
import base64

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
    mesas = Mesa.objects.all()
    return render (request, 'html/admin/gestionMesas.html', {'mesas':mesas})

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
    reservas = Reserva.objects.all()
    return render (request, 'html/admin/ver_reservas.html', {'reservas':reservas})

def agregar_mesa(request):
    if request.method == 'POST':

        datosAgregarMesa = datosAgregarMesaForm(request.POST)
        print(datosAgregarMesa)
        if datosAgregarMesa.is_valid():
            #Limpiar los datos del POST
            numMesaAgg = datosAgregarMesa.cleaned_data['numMesaAgg']
            dispMesaAgg = datosAgregarMesa.cleaned_data['dispMesaAgg']

            #Asignando variables para guardar
            ult_id = Mesa.objects.latest('id_mesa').id_mesa
            id_mesav2 = int(str(ult_id)) + 1
            agg_mesa = Mesa(id_mesav2, numMesaAgg, dispMesaAgg)
            agg_mesa.save()
    else:
            aggMesaForm = MesaForm()
    return render (request, 'html/admin/agregar_mesa.html')


#HTML BODEGA
def gestion_bodega(request):
    return render (request, 'html/bodega/gestion_bodega.html')

def registro_bodega(request):
    return render (request, 'html/bodega/registro_bodega.html')


#HTML CLIENTE
def cliente_hacer_pedido(request):
    platos = Plato.objects.all()

    #arreglo = []

    #for i in platos:
    #    data = {
     #       'data':i.nombre_plato,
      #      'foto':str(base64.b64encode(i.foto), 'utf-8')
       # }
        #arreglo.append(data)

    return render (request, 'html/cliente/cliente_hacer_pedido.html', {'platos' :platos})#data)

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


#Formularios
#Formulario de Hacer Reserva
#def crearReserva(request):
    