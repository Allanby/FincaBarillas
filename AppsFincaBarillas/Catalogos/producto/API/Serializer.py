from rest_framework.serializers import ModelSerializer
from AppsFincaBarillas.Catalogos.producto.models import producto

class ProductoSerializer(ModelSerializer):
    class Meta:
        model = producto
        fields = ['id_producto','codigoCultivo','nombre', 'tipoProductoId', 'FechaSiembra', 'estado']
        # fields = '__all__'