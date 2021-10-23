from django.contrib import admin
from .models import *

class ClientesAdmin (admin.ModelAdmin):
	list_display=("nombre_cliente","apellido_cliente")
		
# Register your models here.

admin.site.register(Cliente)
admin.site.register(Proveedor)
admin.site.register(Mesa)
admin.site.register(Admin)
admin.site.register(Entrega)
admin.site.register(Factura)
admin.site.register(Plato)
admin.site.register(Finanza)
admin.site.register(Pedido)
admin.site.register(Reserva)
admin.site.register(SolicPed)
admin.site.register(Producto)
admin.site.register(Bodega)
admin.site.register(ModoPago)
admin.site.register(Restaurant)
admin.site.register(TipoTrab)
admin.site.register(Trabajador)