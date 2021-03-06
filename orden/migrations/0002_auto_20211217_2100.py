# Generated by Django 3.2.8 on 2021-12-18 00:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0002_auto_20211217_2100'),
        ('orden', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orden',
            name='total',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=9),
        ),
        migrations.CreateModel(
            name='Merma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_merma', models.DateField(auto_now_add=True)),
                ('cant_usada', models.IntegerField()),
                ('producto', models.ForeignKey(blank=True, db_column='id_producto', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='apps.producto')),
            ],
        ),
    ]
