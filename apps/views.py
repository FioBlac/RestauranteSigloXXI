import django
from django import template
from django.shortcuts import render, redirect, get_object_or_404
from .models import Producto, Reserva, Mesa, Plato, AuthUser, Bodega
from datetime import datetime, timedelta
import base64
from .forms import AgregarProductoForm, EliminarProductoForm, EliminarMesaForm, ReservaForm, DatosReservaForm, MesaForm, datosAgregarMesaForm, CustomUserCreationFrom, CustomUserCreationFrom2, EliminarUsuarioForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db.models import Q, query, query_utils
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group, User
from django.http import HttpResponse
from django.db import connection
from django.template.loader import get_template
from django.core.mail import EmailMultiAlternatives, message
from django.conf import settings

# Create your views here.
from .decorators import usuarioPermitido, usuarioNoLogeado, admin_view

def listar_grupos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cur =django_cursor.connection.cursor()

    cursor.callproc("SP_LISTAR_GRUPOS", [out_cur])

    lista = []

    for fila in out_cur:
        lista.append(fila)

    return lista

#HTML GENERAL

def index(request):
    return render (request,'html/general/index.html')

@usuarioNoLogeado
def login_usuario(request):
    storage = messages.get_messages(request)
    for _ in storage:
        # This is important
        # Without this loop _loaded_messages is empty
        pass

    for _ in list(storage._loaded_messages):
        del storage._loaded_messages[0]
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, f'Usuario o contraseña incorrecto')


    return render (request, 'registration/login.html')

def registro(request):

    storage = messages.get_messages(request)
    for _ in storage:
        # This is important
        # Without this loop _loaded_messages is empty
        pass

    for _ in list(storage._loaded_messages):
        del storage._loaded_messages[0]

    data = {
        'form' : CustomUserCreationFrom()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationFrom(data=request.POST)
        if  formulario.is_valid():
            
            if AuthUser.objects.filter(email = formulario.cleaned_data["email"]).exists():
                messages.info(request, f'El correo ya existe')
            else:
                formulario.save()
                email = formulario.cleaned_data["email"]

                #Enviar correo de registro
                sendEmailRegistro(email)
                print(email)


                #agregar usuario a un grupo automaticamente
                usuario = formulario.save()
                group = Group.objects.get(name = 'Cliente')
                usuario.groups.add(group)

                user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
                login(request, user)

                return redirect(to='index')
        data["form"]= formulario

    return render (request, 'registration/registro.html', data)

#@admin_view
def loginAsociado(request):
    storage = messages.get_messages(request)
    for _ in storage:
        # This is important
        # Without this loop _loaded_messages is empty
        pass

    for _ in list(storage._loaded_messages):
        del storage._loaded_messages[0]

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return redirect('index_admin')
        else:
            messages.info(request, f'Usuario o contraseña incorrecto')

    return render (request, 'html/general/loginAsociado.html')

#HTML ADMIN
@login_required(login_url = 'loginAsociado')
@admin_view
def admin_reportes(request):
    return render (request, 'html/admin/admin_reportes.html')

@login_required(login_url = 'loginAsociado')
@admin_view
def agregar_usuario(request):
    storage = messages.get_messages(request)
    for _ in storage:
        # This is important
        # Without this loop _loaded_messages is empty
        pass

    for _ in list(storage._loaded_messages):
        del storage._loaded_messages[0]

    data = {
        'form' : CustomUserCreationFrom(),
        'grupo': listar_grupos()
    }

    if request.method == 'POST':
        formulario = CustomUserCreationFrom2(data=request.POST)
        if  formulario.is_valid():
            
            if AuthUser.objects.filter(email = formulario.cleaned_data["email"]).exists():
                messages.info(request, f'El correo ya existe')
            else:
                formulario.save()
                grupo = request.POST.get('grupo')

                asiGrupo = Group.objects.get(id = grupo)
                usuario = formulario.save()
                usuario.groups.add(asiGrupo)
                

                messages.success(request,'Agregado correctamente')
                return redirect(to='gestion_usuario')
        data["form"]= formulario

    return render (request, 'html/admin/agregar_usuario.html', data)

@login_required(login_url = 'loginAsociado')
@admin_view
def gestion_solicitudes(request):
    return render (request, 'html/admin/gestion_solicitudes.html')

@login_required(login_url = 'loginAsociado')
@admin_view
def gestion_usuario(request):
    storage = messages.get_messages(request)
    for _ in storage:
        # This is important
        # Without this loop _loaded_messages is empty
        pass

    for _ in list(storage._loaded_messages):
        del storage._loaded_messages[0]

    usuarios = AuthUser.objects.all()
    
    if request.method == 'POST':
        usuario_borrar = EliminarUsuarioForm(request.POST)
        
        if usuario_borrar.is_valid():
            id_borrar = usuario_borrar.cleaned_data['id_usuario_borrar']

            User = AuthUser.objects.get(id = id_borrar)
            User.delete()

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

@login_required(login_url = 'loginAsociado')
@admin_view
def gestionMesas(request):
    storage = messages.get_messages(request)
    for _ in storage:
        # This is important
        # Without this loop _loaded_messages is empty
        pass

    for _ in list(storage._loaded_messages):
        del storage._loaded_messages[0]

    mesas = Mesa.objects.all()
    
    if request.method == 'POST':
        mesa_borrar = EliminarMesaForm(request.POST)
        
        if mesa_borrar.is_valid():
            id_borrar = mesa_borrar.cleaned_data['id_mesa_borrar']

            mesa = Mesa.objects.get(id_mesa = id_borrar)
            mesa.delete() 
            messages.success(request,'Eliminado correctamente')
        else:
            print('no funca arriba pq ta malo')

    queryset = request.GET.get("inputBuscarMesa")
    if queryset:
        mesas = Mesa.objects.filter(
            Q(id_mesa__icontains = queryset)
        ).distinct()
    else:
        mesas = Mesa.objects.all()
    return render (request, 'html/admin/gestionMesas.html', {'mesas':mesas})

@login_required(login_url = 'loginAsociado')
@admin_view
def index_admin(request):
    return render (request, 'html/admin/index_admin.html')

@login_required(login_url = 'loginAsociado')
@admin_view
def modificar_usuario(request):
    return render (request, 'html/admin/modificar_usuario.html')

@login_required(login_url = 'loginAsociado')
@admin_view
def solicitud_stock_proveedores(request):
    return render (request, 'html/admin/solicitud_stock_proveedores.html')

@login_required(login_url = 'loginAsociado')
@admin_view
def solicitudes_enviadas(request):
    return render (request, 'html/admin/solicitudes_enviadas.html')

@login_required(login_url = 'loginAsociado')
@admin_view
def solicitudes_recibidas(request):
    return render (request, 'html/admin/solicitudes_recibidas.html')

@login_required(login_url = 'loginAsociado')
@admin_view
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

@login_required(login_url = 'loginAsociado')
@admin_view
def agregar_mesa(request):
    storage = messages.get_messages(request)
    for _ in storage:
        # This is important
        # Without this loop _loaded_messages is empty
        pass

    for _ in list(storage._loaded_messages):
        del storage._loaded_messages[0]

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

            messages.success(request,'Mesa agregada correctamente')
            return redirect(to='gestionMesas')
    else:
            aggMesaForm = MesaForm()
    return render (request, 'html/admin/agregar_mesa.html')


def logoutUserAsoci(request):
    logout(request)
    return redirect('loginAsociado')


#HTML BODEGA
@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Bodega'])
def index_bodeguero(request):      
    return render (request, 'html/bodega/index_bodeguero.html')

@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Bodega'])
def gestion_bodega(request):   
    storage = messages.get_messages(request)
    for _ in storage:
        # This is important
        # Without this loop _loaded_messages is empty
        pass

    for _ in list(storage._loaded_messages):
        del storage._loaded_messages[0]

    productos = Producto.objects.all()
    if request.method == 'POST':
        producto_borrar = EliminarProductoForm(request.POST)
        
        if producto_borrar.is_valid():
            id_borrar = producto_borrar.cleaned_data['id_producto_borrar']

            producto = Producto.objects.get(id_producto = id_borrar)
            producto.delete() 
            messages.success(request,'Producto eliminado correctamente')
            
    return render (request, 'html/bodega/gestion_bodega.html', {'productos':productos})
    

@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Bodega'])
def registro_bodega(request):
    storage = messages.get_messages(request)
    for _ in storage:
        # This is important
        # Without this loop _loaded_messages is empty
        pass

    for _ in list(storage._loaded_messages):
        del storage._loaded_messages[0]

    bodegas = Bodega.objects.all()

    if request.method == 'POST':
        datos_item = AgregarProductoForm(request.POST)

        if datos_item.is_valid():

            id_bodega = datos_item.cleaned_data['id_bodega']
            nombre_alimento = datos_item.cleaned_data['nombre_alimento']
            t_conservacion = datos_item.cleaned_data['t_conservacion']
            cantidad_alimento = datos_item.cleaned_data['cantidad_alimento']
            fecha_caducidad = datos_item.cleaned_data['fecha_caducidad']
            zona_refrigeracion = datos_item.cleaned_data['zona_refrigeracion']
            tipo_alimento = datos_item.cleaned_data['tipo_alimento']

            print(id_bodega)
            print(nombre_alimento)
            print(t_conservacion)
            print(cantidad_alimento)
            print(fecha_caducidad)
            print(zona_refrigeracion)
            print(tipo_alimento)

            #Asignando variables para guardar
            #Tengo que hacer el que pasaria si no hay registros para el id
            try:
                ultimo_id_alimento = Producto.objects.latest('id_producto').id_producto #Último ID registrado en reservas
            except:
                ultimo_id_alimento= 0

            nuevo_id = int(str(ultimo_id_alimento)) + 1 #Se le suma 1

            #Asignar el Id de bodega
            bodega = Bodega.objects.get(id_bodega = id_bodega)

            #bodega_id_bodega
            producto = Producto(
                id_producto  = nuevo_id, 
                bodega_id_bodega = bodega, 
                nombre = nombre_alimento, 
                temperatura_conservacion = t_conservacion, 
                cantidad = cantidad_alimento,
                fecha_caducidad = fecha_caducidad,
                zona_conservacion = zona_refrigeracion,
                tipo_alimento =  tipo_alimento
                )
            producto.save()

            messages.success(request,'Producto agregado correctamente')
            return redirect(to='gestion_bodega')

    return render (request, 'html/bodega/registro_bodega.html', {'bodegas':bodegas})

@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Bodega'])
def solicitud_bodega(request):
    productos = Producto.objects.all()

    return render (request, 'html/bodega/solicitud_bodega.html', {'productos':productos})

#HTML CLIENTE
@login_required(login_url = 'login')
@usuarioPermitido(allowed_roles = ['Cliente'])
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

    return render (request, 'html/cliente/cliente_hacer_pedido.html', {'arreglo' :arreglo})#data

@login_required(login_url = 'login')
@usuarioPermitido(allowed_roles = ['Cliente'])
def cliente_hacer_reserva(request):
    disponibilidad = True
    if request.method == 'POST':

        datos_reserva = DatosReservaForm(request.POST)
        

        if datos_reserva.is_valid():
            #Limpiar los datos del POST
            cantidad_personas = datos_reserva.cleaned_data['cantidad_personas']
            fecha_reserva = datos_reserva.cleaned_data['fecha'].strftime("%Y-%m-%d")
            hora_reserva = datos_reserva.cleaned_data['hora']
            comentario = datos_reserva.cleaned_data['comentario']
            
            print(comentario)

            #Asignando variables para guardar
            #Tengo que hacer el que pasaria si no hay registros para el id
            try:
                ultimo_id = Reserva.objects.latest('id_reserva').id_reserva #Último ID registrado en reservas
            except:
                ultimo_id= 0
            nuevo_id = int(str(ultimo_id)) + 1 #Se le suma 1
            fecha = str(fecha_reserva) + ' ' + str(hora_reserva)
            fecha_vence = datetime.strptime(fecha ,"%Y-%m-%d %H:%M") + timedelta(minutes=20)

            #Asignar mesa que no esté ocupada esa hora.
            todas_reservas = Reserva.objects.all() #Traer todas las reservas
            mesas = Mesa.objects.all() #Traer todas las mesas
            disponibilidad = True
            fecha_busqueda = fecha[:11]  + str(int(fecha[11:13])+3) + fecha[13:] #se le suman 3 horas para solucionar error temporal.
            num_mesa = Mesa.objects.first()
            
            for mesa in mesas:
                for i in todas_reservas:
                    i_reserva = str(i.fecha_reserva)[:16]
                    if  i_reserva == fecha_busqueda : #el i.fecha_reserva es el problema
                        print('Encontró la fecha')
                        
                        while i.id_mesa.id_mesa == mesa.id_mesa:
                            suma_mesa = str(int(mesa.id_mesa)+1) #Se le suma 1 digito a la mesa
                            print(suma_mesa) 
                            try:
                                num_mesa = Mesa.objects.get(id_mesa = suma_mesa)
                                disponibilidad = True
                                print('Asignó la mesa')
                            except:
                                disponibilidad = False
                                print('No hay mesas disponibles') 
                                break
                    else:
                        disponibilidad = True
            
            #Obtener el id del usuario que hace la reserva
            if request.user.is_authenticated:
                id_usuario = AuthUser.objects.get(id = request.user.id) 

            reserva = Reserva(
                id_reserva = nuevo_id, 
                cantidad_personas = cantidad_personas, 
                fecha_reserva = fecha, 
                comentario = comentario, 
                fecha_vence = fecha_vence,
                id_mesa = num_mesa,
                id_usuario = id_usuario
                )

            if disponibilidad == True:
                print("Se guardó")
                reserva.save()         
    else:
        disponibilidad = False
        reserva_form = ReservaForm()
    return render (request, 'html/cliente/cliente_hacer_reserva.html', {'disponibilidad':disponibilidad})

@login_required(login_url = 'login')
@usuarioPermitido(allowed_roles = ['Cliente'])
def cliente_index(request):
    return render (request, 'html/cliente/cliente_index.html')

@login_required(login_url = 'login')
@usuarioPermitido(allowed_roles = ['Cliente'])
def Cliente_Observar_Disponibilidad(request):
    return render (request, 'html/cliente/Cliente_Observar_Disponibilidad.html')

@login_required(login_url = 'login')
@usuarioPermitido(allowed_roles = ['Cliente'])
def cliente_ver_reserva(request):
    reservas = Reserva.objects.all()
    return render (request, 'html/cliente/cliente_ver_reserva.html', {'reservas':reservas})



#HTML GARZON
@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Garzon'])
def main_garzon(request):
    return render (request, 'html/garzon/main_garzon.html')

@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Garzon'])
def retiro_platos(request):
    return render (request, 'html/garzon/retiro_paltos.html')

@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Garzon'])
def ver_reservaciones(request):
    reservas = Reserva.objects.all()

    queryset = request.GET.get("inputBuscarReserva")
    if queryset:
        reservas = Reserva.objects.filter(
            Q(id_reserva__icontains = queryset) |
            Q(comentario__icontains = queryset)
        ).distinct()
    else:
        reservas = Reserva.objects.all()
    return render (request, 'html/garzon/ver_reservaciones.html', {'reservas':reservas})

@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Garzon'])
def detalle(request):
    return render (request, 'html/garzon/detalle.html')


#HTML COCINERO
@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Cocinero'])
def index_cocina(request):
    return render (request, 'html/Cocinero/index_cocina.html')

@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Cocinero'])
def gestion_receta(request):
    return render (request, 'html/Cocinero/gestion_receta.html')

@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Cocinero'])
def ventana_pedidos(request):
    return render (request, 'html/Cocinero/ventana_pedidos.html')

@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Cocinero'])
def ventana_orden_preparacion(request):
    return render (request, 'html/Cocinero/ventana_orden_preparacion.html')

@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Cocinero'])
def pedido_cliente_sin_entrega(request):
    return render (request, 'html/Cocinero/pedido_cliente_sin_entrega.html')


#HTML CONTADOR
@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Contador'])
def index_contador(request):
    return render (request, 'html/Contador/index_contador.html')

@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Contador'])
def movimientos_dinero(request):
    return render (request, 'html/Cocinero/movimientos_dinero.html')


#HTML CAJERO
@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Cajero'])
def index_cajero(request):
    return render (request, 'html/Cajero/index_cajero.html')

@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Cajero'])
def cajero_cuenta_clientes(request):
    return render (request, 'html/Cajero/cajero_cuenta_clientes.html')

@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Cajero'])
def Cobro_Cliente_Manual(request):
    return render (request, 'html/Cajero/Cobro_Cliente_Manual.html')

@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Cajero'])
def pedidos_cajero(request):
    return render (request, 'html/cajero/pedidos_cajero.html')



#ENVIAR CORREO (este es de prueba)

def verificar(request):
    if request.method == 'POST':
        mail = request.POST.get('mail')

        sendEmailReserva(mail)
        print('envio correo')
    return render (request, 'html/general/verificar.html', {})


def sendEmailReserva(username):
    context = {
        'username':username
    }

    template = get_template('html/general/correo.html')
    content = template.render(context)

    correo = EmailMultiAlternatives(
        'Reserva lista!',
        'Su reserva se ha registrado correctamente.',
        settings.EMAIL_HOST_USER,

        #aca va el correo del usuario
        [username]
    )

    correo.attach_alternative(content, 'text/html')
    correo.send()

def sendEmailRegistro(email):
    context = {
        'email': email
    }

    template = get_template('html/general/correo_registro.html')
    content = template.render(context)

    correo = EmailMultiAlternatives(
        'Registro con exito',
        'Usted se ha registrado correctamente en nuestro sitio web.',
        settings.EMAIL_HOST_USER,

        #aca va el correo del usuario
        [email]
    )

    correo.attach_alternative(content, 'text/html')
    correo.send()



def correo(request):
    return render (request, 'html/general/correo.html')


#HTML PAGAR
def metodo_pago(request):
    return render (request, 'html/pago/metodo_pago.html')

def pagar(request):
    return render (request, 'html/pago/pagar.html')
#Formularios
#Formulario de Hacer Reserva
#def crearReserva(request):
    