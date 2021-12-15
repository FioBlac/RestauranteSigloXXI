from .models import Orden
from django.urls import  reverse

def funcionOrden(cart, request):



    orden = Orden.objects.filter(cart=cart).first()

    if orden is None and request.user.is_authenticated:
        orden = Orden.objects.create(cart=cart, user=request.user)

    if orden:
        request.session['orden_id'] = orden.id

    return orden


def breadcrumb(products=True, payment= False, confirmation=False):
    return[
        {'title':'Productos','active':products,'url':reverse('orden')}, 
        {'title':'Pago','active':payment,'url':reverse('orden')}, 
        {'title':'Confirmacion','active':confirmation,'url':reverse('orden')}, 

    ]

def deleteOrden(request):
    request.session['orden_id'] = None