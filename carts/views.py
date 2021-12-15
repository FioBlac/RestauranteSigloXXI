from django.shortcuts import render
from .models import Cart
from  products.models import Product
from .funciones import funcionCarrito
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from .models import CartProduct
from django.contrib import messages

# Create your views here.



def cart(request):
    storage = messages.get_messages(request)
    for _ in storage:
        # This is important
        # Without this loop _loaded_messages is empty
        pass

    for _ in list(storage._loaded_messages):
        del storage._loaded_messages[0]
        
    cart = funcionCarrito(request)
    return render(request,'carts/cart.html',{
        'cart': cart
    })

def add(request):
    storage = messages.get_messages(request)
    for _ in storage:
        # This is important
        # Without this loop _loaded_messages is empty
        pass

    for _ in list(storage._loaded_messages):
        del storage._loaded_messages[0]
        
    cart= funcionCarrito(request)
    product= get_object_or_404 (Product, pk=request.POST.get('product_id'))
    quantity = int(request.POST.get('quantity', 1))

    #cart.products.add(product, through_defaults={'quantity': quantity})
    product_cart = CartProduct.objects.crearActualizar(cart=cart, product=product, quantity=quantity)
    
    return render(request,'carts/add.html',{
        'product': product
    })

def remove(request):
    storage = messages.get_messages(request)
    for _ in storage:
        # This is important
        # Without this loop _loaded_messages is empty
        pass

    for _ in list(storage._loaded_messages):
        del storage._loaded_messages[0]
    
    cart =funcionCarrito(request)
    product= get_object_or_404 (Product, pk=request.POST.get('product_id'))
    cart.products.remove(product)


    return redirect('cart')