from django.contrib import admin
from .models import *
from products.models import Ingredientes
# Register your models here.


admin.site.register(Reserva)
admin.site.register(Boleta)
admin.site.register(Mesa)
admin.site.register(Bodega)
admin.site.register(Ingredientes)
admin.site.register(Producto)

