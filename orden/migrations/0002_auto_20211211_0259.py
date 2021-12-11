# Generated by Django 3.2.8 on 2021-12-11 05:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0001_initial'),
        ('products', '0001_initial'),
        ('orden', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orden',
            name='id_cart',
            field=models.ForeignKey(blank=True, db_column='id_cart_p', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='carts.cart'),
        ),
        migrations.AddField(
            model_name='orden',
            name='id_products',
            field=models.ForeignKey(blank=True, db_column='id_products_p', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='products.product'),
        ),
    ]
