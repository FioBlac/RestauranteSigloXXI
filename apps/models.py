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
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
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


class Boleta(models.Model):
    id_boleta = models.CharField(primary_key=True, max_length=20)
    fecha_emision = models.DateTimeField()
    subtotal = models.BigIntegerField()
    modo_pago_id_modo_pago = models.ForeignKey('ModoPago', models.DO_NOTHING, db_column='modo_pago_id_modo_pago', blank=True, null=True)
    auth_user = models.ForeignKey(AuthUser,  blank=True, null=True, related_name='+', on_delete=models.CASCADE)
    restaurant_rut_rest = models.ForeignKey('Restaurant', models.DO_NOTHING, db_column='restaurant_rut_rest', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'boleta'


class Caja(models.Model):
    id_caja = models.BigIntegerField(primary_key=True)
    boleta_id_boleta = models.ForeignKey(Boleta, on_delete=models.CASCADE, db_column='boleta_id_boleta', blank=True, null=True)
    orden_orden_id_orden = models.ForeignKey('OrdenOrden', models.DO_NOTHING, db_column='orden_orden_id_orden', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'caja'


class CartsCart(models.Model):
    id_cart = models.BigIntegerField(primary_key=True)
    cart_id = models.CharField(unique=True, max_length=100, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField()
    user_id = models.IntegerField(blank=True, null=True)
    auth_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'carts_cart'


class CartsCartproduct(models.Model):
    id_cartproduct = models.BigIntegerField(primary_key=True)
    quantity = models.IntegerField()
    created_at = models.DateTimeField()
    carts_cart_id_cart = models.ForeignKey(CartsCart, models.DO_NOTHING, db_column='carts_cart_id_cart')
    products_product_id_producto = models.ForeignKey('ProductsProduct', models.DO_NOTHING, db_column='products_product_id_producto')

    class Meta:
        managed = False
        db_table = 'carts_cartproduct'


class CategoriesCategory(models.Model):
    id = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=40, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'categories_category'


class CategoriesCategoryProducts(models.Model):
    id = models.BigIntegerField(primary_key=True)
    categories_category = models.ForeignKey(CategoriesCategory, models.DO_NOTHING)
    products_product_id_producto = models.ForeignKey('ProductsProduct', models.DO_NOTHING, db_column='products_product_id_producto')

    class Meta:
        managed = False
        db_table = 'categories_category_products'
        unique_together = (('categories_category', 'products_product_id_producto'),)


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
    hora_entrada = models.CharField(max_length=6)
    hora_salida = models.CharField(max_length=6)
    estado = models.CharField(max_length=50)
    auth_user = models.ForeignKey(AuthUser, related_name='+', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'entrega'


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


class OrdenOrden(models.Model):
    id_orden = models.BigIntegerField(primary_key=True)
    status = models.CharField(max_length=40, blank=True, null=True)
    total = models.DecimalField(max_digits=9, decimal_places=2)
    created_at = models.DateTimeField()
    carts_cart_id_cart = models.ForeignKey(CartsCart, models.DO_NOTHING, db_column='carts_cart_id_cart')
    user_id = models.IntegerField()
    ordenid = models.CharField(unique=True, max_length=100, blank=True, null=True)
    auth_user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    detalle = models.CharField(max_length=200, blank=True, null=True)
    products_product_id_producto = models.ForeignKey('ProductsProduct', models.DO_NOTHING, db_column='products_product_id_producto', blank=True, null=True)
    entrega_id_entrega = models.ForeignKey(Entrega, models.DO_NOTHING, db_column='entrega_id_entrega', blank=True, null=True)
    reserva_id_reserva = models.ForeignKey('Reserva', models.DO_NOTHING, db_column='reserva_id_reserva', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'orden_orden'


class Producto(models.Model):
    id_producto = models.CharField(primary_key=True, max_length=20)
    nombre = models.CharField(max_length=40)
    cantidad = models.CharField(max_length=40)
    temperatura_conservacion = models.FloatField()
    fecha_caducidad = models.DateField()
    zona_conservacion = models.CharField(max_length=40)
    tipo_alimento = models.CharField(max_length=40)
    proveedor_rut_proveedor = models.ForeignKey('Proveedor', models.DO_NOTHING, db_column='proveedor_rut_proveedor', blank=True, null=True)
    bodega_id_bodega = models.ForeignKey(Bodega, models.DO_NOTHING, db_column='bodega_id_bodega', blank=True, null=True)
    solic_ped_id_soli_prod = models.ForeignKey('SolicPed', models.DO_NOTHING, db_column='solic_ped_id_soli_prod', blank=True, null=True)
    products_product_id_producto = models.ForeignKey('ProductsProduct', models.DO_NOTHING, db_column='products_product_id', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'producto'


class ProductsProduct(models.Model):
    id_producto = models.BigIntegerField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    tiempo = models.CharField(max_length=6)
    created_at = models.DateTimeField()
    slug = models.CharField(unique=True, max_length=200, blank=True, null=True)
    image = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products_product'


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
    auth_user = models.ForeignKey(AuthUser, db_column='AUTH_USER_ID', blank=True, null=True, related_name='+', on_delete=models.CASCADE)
    mesa_id_mesa = models.ForeignKey(Mesa, models.DO_NOTHING, db_column='mesa_id_mesa', blank=True, null=True, related_name='+')

    class Meta:
        managed = False
        db_table = 'reserva'


class Restaurant(models.Model):
    rut_rest = models.BigIntegerField(primary_key=True)

class SolicPed(models.Model):
    id_soli_prod = models.CharField(primary_key=True, max_length=20)
    fecha_solicitud = models.DateField()
    hora_solicitud = models.DateTimeField()
    fecha_entrega = models.DateField()
    hora_entrega = models.DateTimeField()
    estado_solicitud = models.CharField(max_length=100)
    auth_user = models.ForeignKey(AuthUser, blank=True, null=True, related_name='+', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'solic_ped'