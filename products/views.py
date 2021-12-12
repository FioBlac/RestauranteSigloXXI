from django.shortcuts import render
from django.views.generic.list import  ListView
from .models import Product
from django.views.generic.detail import  DetailView

# Create your views here.
class ProductListView(ListView):
    template_name ='index_productos.html'
    queryset = Product.objects.all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['mensaje'] = 'Productos'
        return context

class ProductDetailView(DetailView):
    model = Product
    template_name = 'products/product.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
