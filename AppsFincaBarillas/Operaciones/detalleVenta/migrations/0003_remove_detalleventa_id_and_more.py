# Generated by Django 4.2 on 2024-09-26 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('detalleVenta', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detalleventa',
            name='id',
        ),
        migrations.AlterField(
            model_name='detalleventa',
            name='Id_DetalleVenta',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
