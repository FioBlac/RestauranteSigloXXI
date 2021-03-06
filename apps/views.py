from typing import OrderedDict
import django
from django import template
from django.db.models.aggregates import Count
from django.db.models.fields import NullBooleanField
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import translation

from carts.models import CartProduct #from RestauranteSigloXXI.carts.models import CartProduct <-- es el original

#from apps.utils import render_to_pdf
from .models import AuthGroup, AuthUserGroups, Producto, Reserva, Mesa, AuthUser, Bodega
from products.models import Product, Ingredientes
from orden.models import Orden, Merma
#from .models import Pedido, Producto, Reserva, Mesa, Plato, AuthUser, Bodega
from datetime import date, datetime, timedelta
import base64
from .forms import AgregarProductoForm, cambiarEstadoPedidoForm,fechaReporteForm, EliminarProductoForm, EliminarReservaForm, EliminarMesaForm, ReservaForm, DatosReservaForm, MesaForm, datosAgregarMesaForm, CustomUserCreationFrom, CustomUserCreationFrom2, EliminarUsuarioForm
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
from django.db.models import Sum
from apps.forms import crearPlato 
from orden.models import Orden
from products.models import Product

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
            messages.info(request, f'Usuario o contrase??a incorrecto')


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
            messages.info(request, f'Usuario o contrase??a incorrecto')

    return render (request, 'html/general/loginAsociado.html')

#HTML ADMIN
@login_required(login_url = 'loginAsociado')
@admin_view
def admin_reportes(request):
    
    if request.method == 'POST':
        reporteForm = fechaReporteForm(request.POST)

        if reporteForm.is_valid():
            fecha = reporteForm.cleaned_data['mesReporte']
            mesReporte = fecha[:7]
        
            mesas = Mesa.objects.all()
            
            
            


            #Contar Clientes Nuevos
            gruposUsuarios = AuthUserGroups.objects.all()
            grupoCliente = AuthGroup.objects.get(name = 'Cliente')
            contarCliente = 0

            for u in gruposUsuarios:

                if u.group_id == grupoCliente.id:
                    usuarios = AuthUser.objects.get(id = u.user_id)
                    ingresoUsuario = usuarios.date_joined.strftime('%Y-%m')

                    if ingresoUsuario == mesReporte:
                        contarCliente = contarCliente+1
                
            #Contar Reservas Concretadas
            reservas = Reserva.objects.all()
            contarReservas = 0
            for r in reservas:
                fecha_reserva = r.fecha_reserva.strftime('%Y-%m')
                if fecha_reserva == mesReporte:
                    contarReservas = contarReservas +1
                    

            #Contar Ordenes Realizadas
            ordenes = Orden.objects.all()
            contarOrdenes = 0
            for o in ordenes:
                fecha_orden = o.created_at.strftime('%Y-%m')
                if fecha_orden == mesReporte:
                    contarOrdenes = contarOrdenes +1

            #Contar Trabajadores Nuevos
            contarTrabajadores = 0
            for u in gruposUsuarios:
                if u.group_id != grupoCliente.id:
                    contarTrabajadores = contarTrabajadores+1
            
            #Contar Administradores Nuevos
            contarAdministradores = 0
            grupoAdmin = AuthGroup.objects.get(name = 'Admin')
            for u in gruposUsuarios:

                if u.group_id == grupoAdmin.id:
                    usuarios = AuthUser.objects.get(id = u.user_id)
                    ingresoUsuario = usuarios.date_joined.strftime('%Y-%m')

                    if ingresoUsuario == mesReporte:
                        contarAdministradores = contarAdministradores+1
                    

            #Contar Bodegueros Nuevos
            contarBodegueros = 0
            grupoBodega = AuthGroup.objects.get(name = 'Bodega')
            for u in gruposUsuarios:
                if u.group_id == grupoBodega.id:
                    usuarios = AuthUser.objects.get(id = u.user_id)
                    ingresoUsuario = usuarios.date_joined.strftime('%Y-%m')

                    if ingresoUsuario == mesReporte:
                        contarBodegueros = contarBodegueros+1

            #Contar Cajeros Nuevos
            contarCajeros = 0
            grupoCajero = AuthGroup.objects.get(name = 'Cajero')
            for u in gruposUsuarios:
                if u.group_id == grupoCajero.id:
                    usuarios = AuthUser.objects.get(id = u.user_id)
                    ingresoUsuario = usuarios.date_joined.strftime('%Y-%m')

                    if ingresoUsuario == mesReporte:
                        contarCajeros = contarCajeros+1

            #Contar Cocineros Nuevos
            contarCocineros = 0
            grupoCocinero = AuthGroup.objects.get(name = 'Cocinero')
            for u in gruposUsuarios:
                if u.group_id == grupoCocinero.id:
                    usuarios = AuthUser.objects.get(id = u.user_id)
                    ingresoUsuario = usuarios.date_joined.strftime('%Y-%m')

                    if ingresoUsuario == mesReporte:
                        contarCocineros = contarCocineros+1

            #Contar Garzones Nuevos
            contarGarzones = 0
            grupoGarzon = AuthGroup.objects.get(name = 'Garzon')
            for u in gruposUsuarios:
                if u.group_id == grupoGarzon.id:
                    usuarios = AuthUser.objects.get(id = u.user_id)
                    ingresoUsuario = usuarios.date_joined.strftime('%Y-%m')

                    if ingresoUsuario == mesReporte:
                        contarGarzones = contarGarzones+1    

            #Sacar Ganancias del Mes
            totalGanancias = Orden.objects.all()
            ganancias = 0
            for g in totalGanancias:
                fecha_orden = o.created_at.strftime('%Y-%m')

                if g.status != "Cancelado" and fecha_orden == mesReporte:
                    ganancias = ganancias + g.total
            
            #Sacar Gastos del Mes
            mermas = Merma.objects.all()
            totalGastos = 0
            for m in mermas:
                fechaMerma = m.fecha_merma.strftime('%Y-%m')

                if fechaMerma == mesReporte:
                    totalGastos = totalGastos +(m.cant_usada * Producto.objects.get(id = m.producto.id).valor)

            #Sacar Total
            resultadoTotal = ganancias - totalGastos

            return render (request, 'html/admin/reporte.html',{'mesas':mesas, 
            'contarCliente':contarCliente,
            'contarReservas':contarReservas,
            'contarOrdenes':contarOrdenes,
            'contarTrabajadores':contarTrabajadores,
            'contarAdministradores':contarAdministradores,
            'contarBodegueros':contarBodegueros,
            'contarCajeros':contarCajeros,
            'contarCocineros':contarCocineros,
            'contarGarzones':contarGarzones,
            'ganancias':ganancias,
            'totalGastos':totalGastos,
            'resultadoTotal':resultadoTotal})

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
def crear_plato(request):

    storage = messages.get_messages(request)
    for _ in storage:
        # This is important
        # Without this loop _loaded_messages is empty
        pass

    for _ in list(storage._loaded_messages):
        del storage._loaded_messages[0]

    return render (request, 'html/admin/crear_plato.html')


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
        if datosAgregarMesa.is_valid():
            #Limpiar los datos del POST
            #numMesaAgg = datosAgregarMesa.cleaned_data['numMesaAgg']
            dispMesaAgg = datosAgregarMesa.cleaned_data['dispMesaAgg']

            #Asignando variables para guardar
            try:
                ult_id = Mesa.objects.latest('id_mesa').id_mesa #??ltimo ID registrado en las mesas
                ult_num = Mesa.objects.latest('numero_mesa').numero_mesa #??ltimo numero de mesa registrado en mesa
            except:
                ult_id= 0
                ult_num= 0

            id_mesav2 = int(str(ult_id)) + 1
            num_mesa = int(ult_num) + 1
            agg_mesa = Mesa(id_mesav2, num_mesa, dispMesaAgg)
            agg_mesa.save()

            messages.success(request,'Mesa agregada correctamente')
            return redirect(to='gestionMesas')
    else:
            aggMesaForm = MesaForm()
    return render (request, 'html/admin/agregar_mesa.html')


def logoutUserAsoci(request):
    logout(request)
    return redirect('loginAsociado')


@login_required(login_url = 'loginAsociado')
@admin_view
def menu_reportes(request):
    return render(request, 'html/admin/menu_reportes.html')


@login_required(login_url = 'loginAsociado')
@admin_view
def reporte_contable(request):
    id_productos_merma = Merma.objects.filter( fecha_merma = datetime.now()).values_list('producto', flat=True).distinct()
    productos = Producto.objects.filter(id__in = id_productos_merma)

    totalGanancias = 0
    totalPerdidas = 0
    total = 0
    reporteHoy = datetime.now().strftime('%Y-%m-%d')
    ordenSinFecha = Orden.objects.filter( status = 'Completado')
    
    #RECOLECTAR LAS ORDENES HECHAS EN EL DIA
    orden = []
    for tg in ordenSinFecha:
        dia_reporte = tg.created_at.strftime('%Y-%m-%d')

        if dia_reporte == reporteHoy:
            data = {
                'id': tg.id,
                'created_at': tg.created_at,
                'total': tg.total
            }
            orden.append(data)

            totalGanancias = totalGanancias + tg.total


    #RECOLECTAR LOS PRODUCTOS USADOS EN EL DIA
    mermaProduc = []
    for producto in productos:
        cantProducto = Merma.objects.filter(producto = producto, fecha_merma = datetime.now()).aggregate(Sum('cant_usada'))['cant_usada__sum']
        totalProducto = cantProducto * producto.valor

        data = {
            'id': producto.id,
            'nombre': producto.nombre,
            'cant_usada': cantProducto,
            'gastosUnidad': producto.valor,
            'gastosTotal': totalProducto
        }
        mermaProduc.append(data)

        #CALCULAR VALOR DE LAS PERDIDAS
        totalPerdidas = totalPerdidas + totalProducto

    total = totalGanancias - totalPerdidas
    
    return render(request, 'html/admin/reporte_contable.html', {'orden':orden, 
                                                                'totalGanancias':totalGanancias, 
                                                                'totalPerdidas':totalPerdidas,
                                                                'total':total,
                                                                'merma':mermaProduc})


@login_required(login_url = 'loginAsociado')
@admin_view
def reporte_stock(request):
    id_productos_merma = Merma.objects.filter( fecha_merma = datetime.now()).values_list('producto', flat=True).distinct()
    productos = Producto.objects.filter(id__in = id_productos_merma)

    totalPerdidas = 0

    mermaProduc = []
    for producto in productos:
        cantProducto = Merma.objects.filter(producto = producto, fecha_merma = datetime.now()).aggregate(Sum('cant_usada'))['cant_usada__sum']
        totalProducto = cantProducto * producto.valor

        data = {
            'id': producto.id,
            'nombre': producto.nombre,
            'cant_usada': cantProducto,
            'gastosUnidad': producto.valor,
            'gastosTotal': totalProducto
        }
        mermaProduc.append(data)

        #CALCULAR VALOR DE LAS PERDIDAS
        totalPerdidas = totalPerdidas + totalProducto

    return render(request, 'html/admin/reporte_stock.html',{'totalPerdidas':totalPerdidas,
                                                            'merma':mermaProduc})


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

    productos = Producto.objects.all().order_by('id')
    if request.method == 'POST':
        producto_borrar = EliminarProductoForm(request.POST)
        
        if producto_borrar.is_valid():
            id_borrar = producto_borrar.cleaned_data['id_producto_borrar']

            producto = Producto.objects.get(id = id_borrar)
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
            unidad_medida = datos_item.cleaned_data['unidad_medida']
            fecha_caducidad = datos_item.cleaned_data['fecha_caducidad']
            zona_refrigeracion = datos_item.cleaned_data['zona_refrigeracion']
            tipo_alimento = datos_item.cleaned_data['tipo_alimento']
            valor = datos_item.cleaned_data['valor']


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
                ultimo_id_alimento = Producto.objects.latest('id').id #??ltimo ID registrado en reservas
            except:
                ultimo_id_alimento= 0

            nuevo_id = int(str(ultimo_id_alimento)) + 1 #Se le suma 1

            #Asignar el Id de bodega
            bodega = Bodega.objects.get(id_bodega = id_bodega)

            #bodega_id_bodega
            producto = Producto(
                id = nuevo_id, 
                bodega_id_bodega = bodega, 
                nombre = nombre_alimento, 
                temperatura_conservacion = t_conservacion, 
                cantidad = cantidad_alimento,
                unidad_medida = unidad_medida,
                fecha_caducidad = fecha_caducidad,
                zona_conservacion = zona_refrigeracion,
                tipo_alimento =  tipo_alimento,
                valor = valor
                )
            producto.save()

            messages.success(request,'Producto agregado correctamente')
            return redirect(to='gestion_bodega')

    return render (request, 'html/bodega/registro_bodega.html', {'bodegas':bodegas})

@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Bodega'])
def solicitud_bodega(request):
    productos = Producto.objects.all().order_by('id')

    return render (request, 'html/bodega/solicitud_bodega.html', {'productos':productos})

#HTML CLIENTE
@login_required(login_url = 'login')
@usuarioPermitido(allowed_roles = ['Cliente'])
def cliente_hacer_pedido(request):
    return render (request, 'html/cliente/cliente_hacer_pedido.html')#data

@login_required(login_url = 'login')
@usuarioPermitido(allowed_roles = ['Cliente'])
def cliente_hacer_reserva(request):
    respuesta = True
    if request.method == 'POST':
        datos_reserva = DatosReservaForm(request.POST)
        
        if datos_reserva.is_valid():
            respuesta = True
            #Limpiar los datos del POST
            cantidad_personas = datos_reserva.cleaned_data['cantidad_personas']
            fecha_reserva = datos_reserva.cleaned_data['fecha'].strftime("%Y-%m-%d")
            hora_reserva = datos_reserva.cleaned_data['hora']
            comentario = datos_reserva.cleaned_data['comentario']
            
            print(comentario)

            #Asignando variables para guardar
            #Tengo que hacer el que pasaria si no hay registros para el id
            try:
                ultimo_id = Reserva.objects.latest('id_reserva').id_reserva #??ltimo ID registrado en reservas
            except:
                ultimo_id= 0
            nuevo_id = int(str(ultimo_id)) + 1 #Se le suma 1
            fecha = str(fecha_reserva) + ' ' + str(hora_reserva)
            fecha_vence = datetime.strptime(fecha ,"%Y-%m-%d %H:%M") + timedelta(minutes=20)

            #Asignar mesa que no est?? ocupada esa hora.
            todas_reservas = Reserva.objects.all() #Traer todas las reservas
            mesas = Mesa.objects.all() #Traer todas las mesas
            fecha_busqueda = fecha[:11]  + str(int(fecha[11:13])+3) + fecha[13:] #se le suman 3 horas para solucionar error temporal.
            num_mesa = Mesa.objects.first()
            
            for mesa in mesas:
                for i in todas_reservas:
                    i_reserva = str(i.fecha_reserva)[:16]
                    if  i_reserva == fecha_busqueda : #el i.fecha_reserva es el problema
                        print('Encontr?? la fecha')
                        
                        while i.id_mesa.id_mesa == mesa.id_mesa:
                            suma_mesa = str(int(mesa.id_mesa)+1) #Se le suma 1 digito a la mesa
                            print(suma_mesa) 
                            try:
                                num_mesa = Mesa.objects.get(id_mesa = suma_mesa)
                                respuesta = True
                                print('Asign?? la mesa')
                                break
                            except:
                                respuesta = False
                                print('No hay mesas disponibles') 
                                break
                    else:
                        respuesta = True
            
            #Obtener el id del usuario que hace la reserva
            if request.user.is_authenticated:
                usuario = AuthUser.objects.get(id = request.user.id) 

            reserva = Reserva(
                id_reserva = nuevo_id, 
                cantidad_personas = cantidad_personas, 
                fecha_reserva = fecha, 
                comentario = comentario, 
                fecha_vence = fecha_vence,
                mesa_id_mesa = num_mesa,
                auth_user = usuario
                )

            if respuesta == True:
                print("Se guard??")
                reserva.save()    
                respuesta = True 
                print(respuesta) 
        messages.success(request,'??Reserva hecha correctamente! Le recordamos que tiene un plazo de 20 minutos a partir de la fecha y hora de la reserva para llegar al Restaurante. Si no llega, la reserva ser?? cancelada.')
    else:
        reserva_form = ReservaForm()

    disponibilidad = respuesta
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
    reservas = Reserva.objects.all().order_by('id_reserva')
    print("No entr?? al post")

    if request.user.is_authenticated:
        id_usuario = AuthUser.objects.get(id = request.user.id).id

    if request.method == 'POST':
        print("entr?? al post")
        reserva_borrar = EliminarReservaForm(request.POST)
        
        if reserva_borrar.is_valid():
            id_borrar = reserva_borrar.cleaned_data['id_reserva_borrar']

            reserva = Reserva.objects.get(id_reserva = id_borrar)
            reserva.delete() 
            messages.success(request,'Reserva cancelada correctamente')
        else:
            print('no funca arriba pq ta malo')
        
    return render (request, 'html/cliente/cliente_ver_reserva.html', {'reservas':reservas, 'id_usuario':id_usuario})



#HTML GARZON
@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Garzon'])
def main_garzon(request):
    return render (request, 'html/garzon/main_garzon.html')

@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Garzon'])
def retiro_platos(request):
    #OBTENER DATOS PARA MOSTRAR EN LA TABLA
    products = Product.objects.all().order_by('tiempo')
    orden = Orden.objects.all().order_by('id')
    cart = CartProduct.objects.all().order_by('created_at')
    mesas = Mesa.objects.all()
    reservas = Reserva.objects.all()
    print("no entr??")

    if request.method == 'POST':
        print("entr??")
        pedido = cambiarEstadoPedidoForm(request.POST)

        if pedido.is_valid():
            print("es v??lido")
            cambiarEstado = pedido.cleaned_data['cambiarEstado']

            modificar_ped = orden.get(id = cambiarEstado)

            if modificar_ped.status == 'Por Entregar':
                modificar_ped.status = 'Entregado'
                modificar_ped.save()
                messages.success(request,'Plato entregado corectamente')
                print('Si funca')
                
            else:
                print('No funca')
                modificar_ped.status = 'Por Entregar'
                modificar_ped.save()

    return render (request, 'html/garzon/retiro_platos.html', {'orden':orden , 
    'products':products, 
    'cart':cart,
    'reservas':reservas,
    'mesas':mesas } )

@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Garzon'])
def ver_reservaciones(request):
    reservas = Reserva.objects.all()
    mesa = Mesa.objects.all()
    usuario = AuthUser.objects.all()

    queryset = request.GET.get("inputBuscarReserva")
    if queryset:
        reservas = Reserva.objects.filter(
            Q(id_reserva__icontains = queryset) |
            Q(comentario__icontains = queryset)
        ).distinct()
    else:
        reservas = Reserva.objects.all()
    return render (request, 'html/garzon/ver_reservaciones.html', {'reservas':reservas , 'mesa':mesa , 'usuario':usuario})

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
    platos = Product.objects.all().order_by('tiempo')
    cantidadPedido = CartProduct.objects.all().order_by('created_at')
    pedidos = Orden.objects.all().order_by('id')

    if request.method == 'POST':
        pedido = cambiarEstadoPedidoForm(request.POST)
        print('entr?? al post')
        if pedido.is_valid():
            print('post valido')
            cambiarEstado = pedido.cleaned_data['cambiarEstado']

            modificar_ped = pedidos.get(id = cambiarEstado)
            print(cambiarEstado)
            if modificar_ped.status == 'Cocinando':
                print('funcion?? todo')
                modificar_ped.status = 'Por Entregar'
                modificar_ped.save()
                messages.success(request,'Plato listo para su entrega')

            else:
                modificar_ped.status = 'Cocinando'
                modificar_ped.save()          

    return render (request, 'html/Cocinero/ventana_pedidos.html',{'pedidos':pedidos , 'platos':platos , 'cantidadPedido':cantidadPedido })

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
def Cobro_Cliente_Manual(request):
    listapedido = Orden.objects.all()
    return render (request, 'html/Cajero/Cobro_Cliente_Manual.html', {'listapedido':listapedido})
    

@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Cajero'])
def ver_pedidos_historicos(request):
    listacompra = Orden.objects.all()
    return render (request, 'html/cajero/ver_pedidos_historicos.html',{'listacompra':listacompra})

@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Cajero'])
def pedidos_cajero(request):
    return render (request, 'html/cajero/pedidos_cajero.html')

@login_required(login_url = 'loginAsociado')
@usuarioPermitido(allowed_roles = ['Cajero'])
def ListaComprasRealizadas(request):
    listacompra = Orden.objects.all()
    listacompra = Product.objects.all()
    Lista = {'listarcompras':listacompra}
    return render(request, 'apps/templates/Cajero/pedidos_cajero.html', Lista)

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


def manual(request):
    return render (request, 'html/general/manual.html')


#HTML PAGAR
def metodo_pago(request):
    return render (request, 'html/pago/metodo_pago.html')

def pagar(request):
    return render (request, 'html/pago/pagar.html')

def codigoqr(request):
    return render (request, 'html/general/codigoqr.html')


def lista_compras(request):
    orden = Orden.objects.all()
    data = {
        'orden':orden
    }
    return render(request, 'html/Cajero/pedidos_cajero.html', data)













#Formularios
#Formulario de Hacer Reserva
#def crearReserva(request):

#crear PDF
""" from django.shortcuts import render
from django.views.generic import ListView, View
from .models import PedidosHistoricos

class Listapedidoshistoricos(ListView):
    model = PedidosHistoricos
    template_name = "templates/html/Cajero/modelo_pdf.html"
    context_object_name = 'modelo_pdf'  

#Create your views here.
class ListEmpleados(View):
    def get (self, request, *args, **kwargs):
        modelo_pdf = PedidosHistoricos.objects.all()
        data = {
            'modelo_pdf': modelo_pdf
        }
        pdf = render_to_pdf ('') """