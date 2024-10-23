from rest_framework.serializers import ModelSerializer
from AppsFincaBarillas.Operaciones.detalleVenta.models import DetalleVenta

class DetalleVentaSerializer(ModelSerializer):
    class Meta:
        model = DetalleVenta
        fields = ['VentaId','ProductoId','Descripcion', 'Precio_Producto', 'Cantidad_Producto']
        # fields = '__all__'