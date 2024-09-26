from django.db import models
from AppsFincaBarillas.Catalogos.cliente.models import Cliente  # Importa el modelo Cliente correctamente

class Venta(models.Model):
    id_venta = models.AutoField(primary_key=True)  # ID autogenerado
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)  # Relación con la tabla Cliente
    numero_venta = models.CharField(max_length=10, unique=True)  # Número único de venta
    metodo_pago = models.CharField(max_length=50)
    fecha_venta = models.DateTimeField(auto_now_add=True)
    monto_total = models.FloatField()

    def __str__(self):
        return self.numero_venta  # Corrige el método __str__




