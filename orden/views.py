from django.contrib import  messages
from django.shortcuts import render, redirect
from carts.funciones import funcionCarrito, deleteCart
from .models import Orden
from .utils import funcionOrden, deleteOrden
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
   cart = funcionCarrito(request)
   orden = funcionOrden(cart, request)

   return render(request,'orden/orden.html',{
   'cart': cart,
   'orden':orden,
   'breadcrumb': breadcrumb()
   })

@login_required(login_url='login')
def confirmacion(request):
   cart=funcionCarrito(request)
   orden=funcionOrden(cart, request)
   


   return render(request,'orden/confirmacion.html',{
      'cart':cart,
      'orden':orden,
      'breadcrumb':  breadcrumb(confirmation=True),

   })

@login_required(login_url='login')   
def cancelar_orden(request):
   cart=funcionCarrito(request)
   orden=funcionOrden(cart,request)


   if request.user.id != orden.user_id:
      return redirect('index')

   orden.cancelar()
   deleteCart(request)
   deleteOrden(request)

   messages.error(request,'Orden eliminada correctamente')
   return redirect('index')

@login_required(login_url='login') 
def completado(request):
   cart=funcionCarrito(request)
   orden = funcionOrden(cart, request)

   if request.user.id != orden.user_id:
      return redirect('index')

   orden.completado()

   deleteCart(request)
   deleteOrden(request)

   messages.success(request,'Compra realizada ')
   return redirect('index')


