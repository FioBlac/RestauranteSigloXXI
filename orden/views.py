from django.contrib import  messages
from django.shortcuts import render, redirect, get_object_or_404
from carts.funciones import funcionCarrito, deleteCart
from .models import Orden
from .utils import funcionOrden, deleteOrden, funcionRestarIngredientes
from django.contrib.auth.decorators import login_required
from .utils import breadcrumb
from .import views
from django.views.generic.list import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import EmptyQuerySet
from django.contrib.auth.models import User
from .forms import OrdenForm
from apps.models import Reserva
from apps.models import AuthGroup , AuthUserGroups

# Create your views here.


class OrdenViews(LoginRequiredMixin, ListView):
    login_url = 'login'
    template_name ='orden/ordenes.html'

    def get_queryset(self):
        return self.request.user.ordenes_completadas()



@login_required(login_url='login')
def orden (request):
    storage = messages.get_messages(request)
    for _ in storage:
        # This is important
        # Without this loop _loaded_messages is empty
        pass

    for _ in list(storage._loaded_messages):
        del storage._loaded_messages[0]

    reserva_id =request.session.get('reserva_id')
    if reserva_id != None:
        if reserva_id == 'Seleccione su Reserva':
            reserva = None
            cart = funcionCarrito(request)
            orden = funcionOrden(cart, request, reserva)
        else:
            reserva = Reserva.objects.get(id_reserva = reserva_id)
            cart = funcionCarrito(request)
            orden = funcionOrden(cart, request, reserva)
    else:
        cart = funcionCarrito(request)
        orden = funcionOrden(cart, request, None)
    


    return render(request,'orden/orden.html',{
    'cart': cart,
    'orden':orden,
    'breadcrumb': breadcrumb()
    })

@login_required(login_url='login')
def confirmacion(request):
    storage = messages.get_messages(request)
    grupo = AuthGroup.objects.get(name='Garzon')
    grupos= AuthUserGroups.objects.filter(group__id=grupo.id)
    for _ in storage:
        # This is important
        # Without this loop _loaded_messages is empty
        pass

    for _ in list(storage._loaded_messages):
        del storage._loaded_messages[0]

    cart=funcionCarrito(request)
    orden=funcionOrden(cart, request)

    #Aquí se registra los ingredientes utilizados en el pedido
    funcionRestarIngredientes(cart)
    #Termina el registro de los ingredientes


    return render(request,'orden/confirmacion.html',{
        'cart':cart,
        'orden':orden,
        'grupos' : grupos,
        'breadcrumb':  breadcrumb(confirmation=True),
    })
	
@login_required(login_url='login')   
def cancelar_orden(request):
    storage = messages.get_messages(request)
    for _ in storage:
        # This is important
        # Without this loop _loaded_messages is empty
        pass

    for _ in list(storage._loaded_messages):
        del storage._loaded_messages[0]
        
    cart=funcionCarrito(request)
    orden=funcionOrden(cart,request,None)


    if request.user.id != orden.user_id:
            return redirect('index_productos')

    orden.cancelar()
    deleteCart(request)
    deleteOrden(request)

    messages.error(request,'Orden eliminada correctamente')
    return redirect('index_productos')

@login_required(login_url='login') 
def completado(request):
    storage = messages.get_messages(request)
    for _ in storage:
        # This is important
        # Without this loop _loaded_messages is empty
        pass

    for _ in list(storage._loaded_messages):
        del storage._loaded_messages[0]
        
    cart=funcionCarrito(request)
    orden = funcionOrden(cart, request, None)

    if request.user.id != orden.user_id:
        return redirect('index_productos')

    orden.completado()

    deleteCart(request)
    deleteOrden(request)

    messages.success(request,'Compra realizada ')
    return redirect('index_productos')

def listar_orden(request):
    orden = Orden.objects.all()

    data ={
        'orden' : orden
    }


    return render(request,'orden/listar_orden.html',data)




def modificar_orden(request,id):

    orden= get_object_or_404(Orden, id=id)

    data={

        'form': OrdenForm(instance=orden)
    }
    if request.method == 'POST':
        formulario = OrdenForm(data=request.POST, instance=orden,files=request.FILES)
        if formulario.is_valid():
            formulario.save()
            return redirect(to="confirmacion")
        data["form"] = formulario
   
    
    return render(request,'orden/editar_orden.html',data)




