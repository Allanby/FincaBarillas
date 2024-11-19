from rest_framework.serializers import ModelSerializer
from AppsFincaBarillas.Operaciones.detalleVenta.models import DetalleVenta

class DetalleVentaSerializer(ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = ['Id_DetalleVenta','venta','producto', 'descripcion', 'precio_producto', 'cantidad_producto']
        # fields = '__all__'