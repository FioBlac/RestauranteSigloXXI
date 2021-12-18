from django.contrib import  messages
from django.shortcuts import render, redirect
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

    cart = funcionCarrito(request)
    orden = funcionOrden(cart, request)
    


    return render(request,'orden/orden.html',{
    'cart': cart,
    'orden':orden,
    'breadcrumb': breadcrumb()
    })

@login_required(login_url='login')
def confirmacion(request):
    storage = messages.get_messages(request)
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
    orden=funcionOrden(cart,request)


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
    orden = funcionOrden(cart, request)

    if request.user.id != orden.user_id:
        return redirect('index_productos')

    orden.completado()

    deleteCart(request)
    deleteOrden(request)

    messages.success(request,'Compra realizada ')
    return redirect('index_productos')


