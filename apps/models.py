from django.db import models

# Create your models here.
class Admin(models.Model):
    rut_admin = models.CharField(primary_key=True, max_length=20)
    nombre_admin = models.CharField(max_length=40)
    apellido_admin = models.CharField(max_length=40)
    email_admin = models.CharField(max_length=40)
    password_admin = models.CharField(max_length=40)
    telefono_admin = models.CharField(max_length=15)
    tipo_admin = models.CharField(max_length=40)
    fecha_contra_admin = models.DateField()

    class Meta:
        managed = False
        db_table = 'admin'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(max_length=254, blank=True, null=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Bodega(models.Model):
    id_bodega = models.CharField(primary_key=True, max_length=20)
    total_producto = models.CharField(max_length=200)
    total_merma = models.CharField(max_length=100)
    categoria_producto = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'bodega'


class Cliente(models.Model):
    rut_cliente = models.CharField(primary_key=True, max_length=20)
    nombre_cliente = models.CharField(max_length=40)
    apellido_cliente = models.CharField(max_length=40)
    email_cliente = models.CharField(max_length=40)
    password_cliente = models.CharField(max_length=40)
    telefono_cliente = models.CharField(max_length=15)

    class Meta:
        managed = False
        db_table = 'cliente'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200, blank=True, null=True)
    action_flag = models.IntegerField()
    change_message = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField(blank=True, null=True)
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Entrega(models.Model):
    id_entrega = models.BigIntegerField(primary_key=True)
    hora_entrada = models.DateTimeField()
    hora_salida = models.DateTimeField()
    estado = models.CharField(max_length=50)
    trabajador_rut_trab = models.ForeignKey('Trabajador', models.DO_NOTHING, db_column='trabajador_rut_trab', blank=True, null=True,related_name='+')
    pedido_id_pedido = models.ForeignKey('Pedido', models.DO_NOTHING, db_column='pedido_id_pedido', blank=True, null=True,related_name='+')

    class Meta:
        managed = False
        db_table = 'entrega'


class Factura(models.Model):
    id_boleta = models.CharField(primary_key=True, max_length=20)
    fecha_emision = models.DateTimeField()
    subtotal = models.BigIntegerField()
    cliente_rut_cliente = models.ForeignKey(Cliente, models.DO_NOTHING, db_column='cliente_rut_cliente', blank=True, null=True)
    modo_pago_id_modo_pago = models.ForeignKey('ModoPago', models.DO_NOTHING, db_column='modo_pago_id_modo_pago', blank=True, null=True,related_name='+')
    restaurant_rut_rest = models.ForeignKey('Restaurant', models.DO_NOTHING, db_column='restaurant_rut_rest', blank=True, null=True,related_name='+')
    finanza_rut_finan = models.ForeignKey('Finanza', models.DO_NOTHING, db_column='finanza_rut_finan', blank=True, null=True,related_name='+')

    class Meta:
        managed = False
        db_table = 'factura'


class Finanza(models.Model):
    rut_finan = models.CharField(primary_key=True, max_length=20)
    nombre_finan = models.CharField(max_length=40)
    apellido_finan = models.CharField(max_length=40)
    email_finan = models.CharField(max_length=40)
    password_finan = models.CharField(max_length=40)
    telefono_finan = models.CharField(max_length=15)
    fecha_contra_finan = models.DateField()

    class Meta:
        managed = False
        db_table = 'finanza'


class Mesa(models.Model):
    id_mesa = models.CharField(primary_key=True, max_length=20)
    numero_mesa = models.BigIntegerField()
    disponibilidad = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'mesa'


class ModoPago(models.Model):
    id_modo_pago = models.BigIntegerField(primary_key=True)
    denominacion = models.CharField(max_length=60)

    class Meta:
        managed = False
        db_table = 'modo_pago'


class Pedido(models.Model):
    id_pedido = models.CharField(primary_key=True, max_length=20)
    cantidad = models.BigIntegerField()
    precio_ampliado = models.BigIntegerField()
    total = models.BigIntegerField()
    mesa_id_mesa = models.ForeignKey(Mesa, models.DO_NOTHING, db_column='mesa_id_mesa', blank=True, null=True)
    reserva_id_reserva = models.ForeignKey('Reserva', models.DO_NOTHING, db_column='reserva_id_reserva', blank=True, null=True,related_name='+')
    factura_id_boleta = models.ForeignKey(Factura, models.DO_NOTHING, db_column='factura_id_boleta', blank=True, null=True,related_name='+')
    plato_id_plato = models.ForeignKey('Plato', models.DO_NOTHING, db_column='plato_id_plato', blank=True, null=True,related_name='+')
    entrega_id_entrega = models.ForeignKey(Entrega, models.DO_NOTHING, db_column='entrega_id_entrega', blank=True, null=True,related_name='+')

    class Meta:
        managed = False
        db_table = 'pedido'


class Plato(models.Model):
    id_plato = models.CharField(primary_key=True, max_length=20)
    nombre_plato = models.CharField(max_length=40)
    precio = models.FloatField()
    tipo_plato = models.CharField(max_length=50)
    tiempo_prepar = models.DateField()

    class Meta:
        managed = False
        db_table = 'plato'


class Producto(models.Model):
    id_producto = models.CharField(primary_key=True, max_length=20)
    nombre = models.CharField(max_length=40)
    cantidad = models.CharField(max_length=40)
    temperatura_conservacion = models.FloatField()
    fecha_caducidad = models.DateField()
    zona_conservacion = models.CharField(max_length=40)
    tipo_alimento = models.CharField(max_length=40)
    proveedor_rut_proveedor = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='proveedor_rut_proveedor', blank=True, null=True,related_name='+')       
    bodega_id_bodega = models.ForeignKey(Bodega, models.DO_NOTHING, db_column='bodega_id_bodega', blank=True, null=True,related_name='+')
    plato_id_plato = models.ForeignKey(Plato, models.DO_NOTHING, db_column='plato_id_plato', blank=True, null=True,related_name='+')
    solic_ped_id_soli_prod = models.ForeignKey('SolicPed', models.DO_NOTHING, db_column='solic_ped_id_soli_prod', blank=True, null=True,related_name='+')

    class Meta:
        managed = False
        db_table = 'producto'


class Proveedor(models.Model):
    rut_proveedor = models.CharField(primary_key=True, max_length=20)
    nombre_proveedor = models.CharField(max_length=40)
    direccion_proveedor = models.CharField(max_length=40)
    codigo_postal = models.BigIntegerField()
    ciudad = models.CharField(max_length=20)
    pais = models.CharField(max_length=20)
    telefono_proveedor = models.CharField(max_length=20)
    email_proveedor = models.CharField(max_length=40)

    class Meta:
        managed = False
        db_table = 'proveedor'


class Reserva(models.Model):
    id_reserva = models.CharField(primary_key=True, max_length=20)
    cantidad_personas = models.BigIntegerField()
    fecha_reserva = models.DateTimeField()
    comentario = models.CharField(max_length=200, blank=True, null=True)
    fecha_vence = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'reserva'


class Restaurant(models.Model):
    rut_rest = models.BigIntegerField(primary_key=True)
    nombre_rest = models.CharField(max_length=100)
    direccion_rest = models.CharField(max_length=40)
    telefono = models.CharField(max_length=15)
    factura_id_boleta = models.ForeignKey(Factura, models.DO_NOTHING, db_column='factura_id_boleta', blank=True, null=True,related_name='+')

    class Meta:
        managed = False
        db_table = 'restaurant'


class SolicPed(models.Model):
    id_soli_prod = models.CharField(primary_key=True, max_length=20)
    fecha_solicitud = models.DateField()
    hora_solicitud = models.DateTimeField()
    fecha_entrega = models.DateField()
    hora_entrega = models.DateTimeField()
    estado_solicitud = models.CharField(max_length=100)
    admin_rut_admin = models.ForeignKey(Admin, models.DO_NOTHING, db_column='admin_rut_admin', blank=True, null=True,related_name='+')

    class Meta:
        managed = False
        db_table = 'solic_ped'


class TipoTrab(models.Model):
    id_tipo_trab = models.BigIntegerField()
    descripcion = models.CharField(max_length=50)
    trabajador_rut_trab = models.ForeignKey('Trabajador', models.DO_NOTHING, db_column='trabajador_rut_trab', blank=True, null=True,related_name='+')
    tipo_trab_id = models.FloatField(primary_key=True)

    class Meta:
        managed = False
        db_table = 'tipo_trab'


class Trabajador(models.Model):
    rut_trab = models.CharField(primary_key=True, max_length=20)
    nombre_trab = models.CharField(max_length=40)
    apellido_trab = models.CharField(max_length=40)
    email_trab = models.CharField(max_length=40)
    password_trab = models.CharField(max_length=40)
    telefono_trab = models.CharField(max_length=15)
    fecha_contra_trab = models.DateField()
    tipo_trab_tipo_trab = models.ForeignKey(TipoTrab, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'trabajador'