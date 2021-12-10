from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import  login as lg
from django.contrib.auth import  authenticate
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import  logout
from .forms import  Registro
from django.contrib.auth.models import User
from products.models import Product
from django.http import HttpResponseRedirect


def index (request):
    productos=Product.objects.all()
    return render(request,'index.html',{
        'productos':productos,
    })
    

def salir(request):
    logout(request)
    messages.success(request,'Sesion cerrada')
    return redirect('index')

