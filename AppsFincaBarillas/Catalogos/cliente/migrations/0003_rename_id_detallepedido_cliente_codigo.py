# Generated by Django 4.2 on 2024-09-26 02:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0002_rename_codigo_cliente_id_detallepedido'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cliente',
            old_name='id_DetallePedido',
            new_name='codigo',
        ),
    ]
