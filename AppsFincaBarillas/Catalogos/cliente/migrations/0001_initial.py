# Generated by Django 4.2 on 2024-09-11 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=6)),
                ('nombres', models.CharField(max_length=32)),
                ('apellidos', models.CharField(max_length=50)),
                ('telefono', models.CharField(max_length=28)),
                ('direccion', models.TextField()),
                ('estado', models.SmallIntegerField()),
            ],
        ),
    ]
