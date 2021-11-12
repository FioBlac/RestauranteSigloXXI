from django.urls import path
#from .views import home, login
from . import views


urlpatterns =[
    #HTML GENERAL
    path('', views.index, name='index'),
    path('login', views.login_usuario, name='login'),
    path('registro', views.registro, name='registro'),

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
    path('eliminar_usuario/<id>/', views.eliminar_usuario, name= 'eliminar_usuario'),
    path('logoutUserAsoci', views.logoutUserAsoci, name= 'logoutUserAsoci'),

    #HTML BODEGA
    path('gestion_bodega', views.gestion_bodega, name='gestion_bodega'),
    path('registro_bodega', views.registro_bodega, name='registro_bodega'),
    path('index_bodeguero', views.index_bodeguero, name='index_bodeguero'),

    #HTML CLIENTE
    path('cliente_hacer_pedido', views.cliente_hacer_pedido, name='cliente_hacer_pedido'),
    path('cliente_hacer_reserva', views.cliente_hacer_reserva, name='cliente_hacer_reserva'),
    path('cliente_index', views.cliente_index, name='cliente_index'),
    path('Cliente_Observar_Disponibilidad', views.Cliente_Observar_Disponibilidad, name='Cliente_Observar_Disponibilidad'),
    path('cliente_ver_reserva', views.cliente_ver_reserva, name='cliente_ver_reserva'),

    #HTML GARZON
    path('main_garzon', views.main_garzon, name='main_garzon'),
    path('retiro_platos', views.retiro_platos, name='retiro_platos'),
    path('ver_reservas', views.ver_reservas, name='ver_reservas'),

    #HTML COCINERO
    path('index_cocina', views.index_cocina, name='index_cocina'),
    path('gestion_receta', views.gestion_receta, name='gestion_receta'),

    #HTML CAJERO
    path('cajero_cuenta_clientes', views.cajero_cuenta_clientes, name='cajero_cuenta_clientes'),
    path('cobro_cliente_manual', views.cobro_cliente_manual, name='cobro_cliente_manual'),
    path('index_cajero', views.index_cajero, name='index_cajero'),

    #HTML CONTADOR
    path('index_contador', views.index_contador, name='index_contador'),
    path('movimientos_dinero', views.movimientos_dinero, name='movimientos_dinero'),
    path('verificar', views.verificar, name='verificar'),
    path('correo', views.correo, name='correo'),
]