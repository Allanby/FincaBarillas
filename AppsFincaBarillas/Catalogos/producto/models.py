from django.db import models
from AppsFincaBarillas.Catalogos.TipoProducto.models import TipoProducto

class producto(models.Model):
    id_producto = models.IntegerField(primary_key=True)
    codigoCultivo = models.CharField(max_length=6)
    nombre = models.CharField(max_length=32)
    tipoProductoId = models.ForeignKey(TipoProducto, on_delete=models.RESTRICT)
    FechaSiembra = models.DateTimeField(auto_now_add=True)
    estado = models.CharField(max_length=32)

    def __str__(self):
        return f'{self.codigoCultivo}-{self.nombre}'

    class Meta:
        db_table = 'producto_producto'  # Asegúrate de que el nombre de la tabla es correcto

