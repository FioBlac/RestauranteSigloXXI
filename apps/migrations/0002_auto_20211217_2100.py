# Generated by Django 3.2.8 on 2021-12-18 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='unidad_medida',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='producto',
            name='valor',
            field=models.IntegerField(null=True),
        ),
    ]