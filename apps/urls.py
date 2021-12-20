from os import name
from django import urls
from django.urls import path
#from .views import home, login
from . import views
from apps.views import lista_compras

urlpatterns =[
    #HTML GENERAL
    path('', views.index, name='index'),
    path('login', views.login_usuario, name='login'),
    path('registro', views.registro, name='registro'),
    path('codigoqr', views.codigoqr, name='codigoqr'),

    path('manual', views.manual, name='manual'),

    path('loginAsociado', views.loginAsociado, name='loginAsociado'),

    #HTML ADMIN
    path('admin_reportes', views.admin_reportes, name='admin_reportes'),
    path('agregar_usuario', views.agregar_usuario, name='agregar_usuario'),
    path('gestion_solicitudes', views.gestion_solicitudes, name='gestion_solicitudes'),
    path('gestion_usuario', views.gestion_usuario, name='gestion_usuario'),
    path('gestionMesas', views.gestionMesas, name='gestionMesas'),
    path('index_admin', views.index_admin, name='index_admin'),
    path('modificar_usuario', views.modificar_usuario, name='modificar_usuario'),
    path('solicitud_stock_proveedores', views.solicitud_stock_proveedores, name='solicitud_stock_proveedores'),
    path('solicitudes_enviadas', views.solicitudes_enviadas, name='solicitudes_enviadas'),
    path('solicitudes_recibidas', views.solicitudes_recibidas, name='solicitudes_recibidas'),
    path('ver_reservas', views.ver_reservas, name='ver_reservas'),
    path('agregar_mesa', views.agregar_mesa, name='agregar_mesa'),
    path('logoutUserAsoci', views.logoutUserAsoci, name= 'logoutUserAsoci'),
    path('crear_plato', views.crear_plato, name= 'crear_plato'),
    path('reporte_contable', views.reporte_contable, name= 'reporte_contable'),
    path('reporte_stock', views.reporte_stock, name= 'reporte_stock'),
    path('menu_reportes', views.menu_reportes, name= 'menu_reportes'),

    #HTML BODEGA
    path('gestion_bodega', views.gestion_bodega, name='gestion_bodega'),
    path('registro_bodega', views.registro_bodega, name='registro_bodega'),
    path('index_bodeguero', views.index_bodeguero, name='index_bodeguero'),
    path('solicitud_bodega', views.solicitud_bodega, name='solicitud_bodega'),

    #HTML CLIENTE
    path('cliente_hacer_pedido', views.cliente_hacer_pedido, name='cliente_hacer_pedido'),
    path('cliente_hacer_reserva', views.cliente_hacer_reserva, name='cliente_hacer_reserva'),
    path('cliente_index', views.cliente_index, name='cliente_index'),
    path('Cliente_Observar_Disponibilidad', views.Cliente_Observar_Disponibilidad, name='Cliente_Observar_Disponibilidad'),
    path('cliente_ver_reserva', views.cliente_ver_reserva, name='cliente_ver_reserva'),

    #HTML GARZON
    path('main_garzon', views.main_garzon, name='main_garzon'),
    path('retiro_platos', views.retiro_platos, name='retiro_platos'),
    path('ver_reservaciones', views.ver_reservaciones, name='ver_reservaciones'),
    path('detalle', views.detalle, name='detalle'),

    #HTML COCINERO
    path('index_cocina', views.index_cocina, name='index_cocina'),
    path('gestion_receta', views.gestion_receta, name='gestion_receta'),
    path('ventana_pedidos', views.ventana_pedidos, name='ventana_pedidos'),
    path('ventana_orden_preparacion', views.ventana_orden_preparacion, name='ventana_orden_preparacion'),
    path('pedido_cliente_sin_entrega', views.pedido_cliente_sin_entrega, name='pedido_cliente_sin_entrega'),
    path('pedido_cajero',views.ListaComprasRealizadas, name= 'pedido_cajero'),
    
    #HTML CAJERO
    path('Cobro_Cliente_Manual', views.Cobro_Cliente_Manual, name='Cobro_Cliente_Manual'),
    path('index_cajero', views.index_cajero, name='index_cajero'),
    #path('pedidos_cajero', views.pedidos_cajero, name='pedidos_cajero'),
    path('ver_pedidos_historicos',views.ver_pedidos_historicos, name='ver_pedidos_historicos'),
    path('lista_compras',lista_compras, name= 'lista_compras'),

    #HTML CONTADOR
    path('index_contador', views.index_contador, name='index_contador'),
    path('movimientos_dinero', views.movimientos_dinero, name='movimientos_dinero'),
    path('correo', views.correo, name='correo'),

    #HTML DE PAGO
    path('metodo_pago',views.metodo_pago , name= 'metodo_pago'),
    path('pagar',views.pagar , name= 'pagar')
]
""" #url.py
from django.contrib import admin
from . import views

app_name = "persona_app"

urlpatterns = {
    path(
        'lista/',
        views.Listapedidoshistoricos.as_view(),
        name= 'Lista'
        ),
} """