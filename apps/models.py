# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import base64



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


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auth_permission'


class AuthUser(models.Model):
    password = models.CharField(max_length=128, blank=True, null=True)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, blank=True, null=True)
    first_name = models.CharField(max_length=150, blank=True, null=True)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    email = models.CharField(unique=True, max_length=254, blank=True, null=True)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'


class Bodega(models.Model):
    id_bodega = models.CharField(primary_key=True, max_length=20)
    total_producto = models.CharField(max_length=200)
    total_merma = models.CharField(max_length=100)
    categoria_producto = models.CharField(max_length=100)

    def __str__(self):
        return self.categoria_producto



class Boleta(models.Model):
    id_boleta = models.CharField(primary_key=True, max_length=20)
    fecha_emision = models.DateTimeField()
    subtotal = models.BigIntegerField()
    auth_user = models.ForeignKey(AuthUser,  blank=True, null=True, related_name='+', on_delete=models.CASCADE)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200, blank=True, null=True)
    action_flag = models.IntegerField()
    change_message = models.TextField(blank=True, null=True)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True, related_name='+')
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, blank=True, null=True)
    model = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'django_content_type'


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


class Mesa(models.Model):
    id_mesa = models.CharField(primary_key=True, max_length=20)
    numero_mesa = models.BigIntegerField()
    disponibilidad = models.CharField(max_length=50)


class Producto(models.Model):
    id = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=40)
    cantidad = models.CharField(max_length=40)
    unidad_medida = models.CharField(max_length=20, null=True)
    temperatura_conservacion = models.FloatField()
    fecha_caducidad = models.DateField()
    zona_conservacion = models.CharField(max_length=40)
    tipo_alimento = models.CharField(max_length=40)
    valor = models.IntegerField(null=True)
    proveedor_rut_proveedor = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='proveedor_rut_proveedor', blank=True, null=True)
    bodega_id_bodega = models.ForeignKey(Bodega, models.DO_NOTHING, db_column='bodega_id_bodega', blank=True, null=True)
    solic_ped_id_soli_prod = models.ForeignKey('SolicPed', models.DO_NOTHING, db_column='solic_ped_id_soli_prod', blank=True, null=True)

    def __str__(self):
        return self.nombre

class Proveedor(models.Model):
    rut_proveedor = models.CharField(primary_key=True, max_length=20)
    nombre_proveedor = models.CharField(max_length=40)
    direccion_proveedor = models.CharField(max_length=40)
    codigo_postal = models.BigIntegerField()
    ciudad = models.CharField(max_length=20)
    pais = models.CharField(max_length=20)
    telefono_proveedor = models.CharField(max_length=20)
    email_proveedor = models.CharField(max_length=40)

class Reserva(models.Model):
    id_reserva = models.CharField(primary_key=True, max_length=20)
    cantidad_personas = models.BigIntegerField()
    fecha_reserva = models.DateTimeField()
    comentario = models.CharField(max_length=200, blank=True, null=True)
    fecha_vence = models.DateTimeField()
    auth_user = models.ForeignKey(AuthUser, db_column='AUTH_USER_ID', blank=True, null=True, related_name='+', on_delete=models.CASCADE)
    mesa_id_mesa = models.ForeignKey(Mesa, models.DO_NOTHING, db_column='mesa_id_mesa', blank=True, null=True, related_name='+')


class SolicPed(models.Model):
    id_soli_prod = models.CharField(primary_key=True, max_length=20)
    producto_pedir = models.CharField(max_length = 100)
    cantidad = models.CharField(max_length = 100)
    fecha_solicitud = models.DateField()
    hora_solicitud = models.DateTimeField()
    fecha_entrega = models.DateField()
    hora_entrega = models.DateTimeField()
    estado_solicitud = models.CharField(max_length=100)
    auth_user = models.ForeignKey(AuthUser, blank=True, null=True, related_name='+', on_delete=models.CASCADE)