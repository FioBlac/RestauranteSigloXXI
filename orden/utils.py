from apps.models import Producto
from carts.models import CartProduct
from products.models import Ingredientes
from .models import Orden, Merma
from django.urls import  reverse

def funcionOrden(cart, request, reserva):
    orden = Orden.objects.filter(cart=cart).first()

    if orden is None and request.user.is_authenticated:
        orden = Orden.objects.create(cart=cart, user=request.user, id_reserva = reserva)
        request.session['reserva_id'] = None

    if orden:
        request.session['orden_id'] = orden.id
    return orden

#Esta funcion la hizo el Jose
def funcionRestarIngredientes(cart):
    platosCarrito = CartProduct.objects.filter(cart=cart)

    for p in platosCarrito:
        numPlatos = p.quantity
        while numPlatos > 0:
            numPlatos = numPlatos - 1
            ingredientes = Ingredientes.objects.filter(product = p.product)
            print(ingredientes)

            for i in ingredientes:
                cantidadIngredientes = i.cantidad
                ingrediente= Producto.objects.get(id = i.producto.id)
                ingrediente.cantidad =  int(ingrediente.cantidad) - int(cantidadIngredientes)
                ingrediente.save()

                
                #merma.producto = ingrediente
                #merma.cant_usada = i.cantidad
                merma = Merma.objects.create(producto = ingrediente, cant_usada = i.cantidad)
                #merma.save()

        

def breadcrumb(products=True, payment= False, confirmation=False):
    return[
        {'title':'Productos','active':products,'url':reverse('orden')}, 
        {'title':'Pago','active':payment,'url':reverse('orden')}, 
        {'title':'Confirmacion','active':confirmation,'url':reverse('orden')}, 

    ]

def deleteOrden(request):
    request.session['orden_id'] = None