from django.db import models

class Cliente(models.Model):  # Nombres de clases en PascalCase
    codigo = models.CharField(max_length=6)  # Código único del cliente
    nombres = models.CharField(max_length=32)
    apellidos = models.CharField(max_length=50)
    telefono = models.CharField(max_length=28)
    direccion = models.TextField()
    estado = models.SmallIntegerField()

    def __str__(self):
        return self.codigo  # Devuelve el nombre del cliente para las representaciones

