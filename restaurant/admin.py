from django.contrib import admin
from .models import *

class ClientesAdmin (admin.ModelAdmin):
	list_display=("nombre_cliente","apellido_cliente")
		
# Register your models here.
admin.site.register(Proveedor)
admin.site.register(Mesa)
admin.site.register(Cliente,ClientesAdmin)
admin.site.register(Boleta)
admin.site.register(Plato)
admin.site.register(Pedido)
admin.site.register(Reserva)
admin.site.register(SolicPed)
admin.site.register(Producto)
admin.site.register(Bodega)
admin.site.register(Admin)
admin.site.register(Colab)
