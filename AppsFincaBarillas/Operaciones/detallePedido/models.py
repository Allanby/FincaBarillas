from django.db import models
from AppsFincaBarillas.Operaciones.pedidos.models import Pedidos
from AppsFincaBarillas.Catalogos.producto.models import producto

class DetallePedido(models.Model):
    id = models.IntegerField(primary_key=True)  # ID autogenerado para el detalle
    pedido = models.ForeignKey(Pedidos, on_delete=models.CASCADE)  # Clave foránea a la tabla Pedidos
    producto = models.ForeignKey(producto, on_delete=models.CASCADE)  # Clave foránea a la tabla Productos
    cantidad = models.IntegerField()

    def __str__(self):
        return str(self.id)


def detallePedido():
    return None