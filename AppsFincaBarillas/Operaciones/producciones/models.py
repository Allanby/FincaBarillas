from django.db import models
from AppsFincaBarillas.Catalogos.producto.models import producto

class Producciones(models.Model):
    Id_produccion = models.IntegerField(primary_key=True)
    codigo_produccion = models.CharField(max_length=32)
    producto = models.ForeignKey(producto, on_delete=models.CASCADE)
    calidad_cosecha = models.CharField(max_length=50)
    fecha_produccion = models.DateTimeField(auto_now_add=True)
    cantidad_producida = models.SmallIntegerField()
    lapso_produccion = models.DurationField()

    def __str__(self):
        return self.codigo_produccion


def producciones():
    return None