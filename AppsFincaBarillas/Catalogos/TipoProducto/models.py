from django.db import models

class TipoProducto(models.Model):
    codigo = models.CharField(max_length=6)
    description = models.CharField(max_length=100)

    def __str__(self):
        return self.description


# Create your models here.
