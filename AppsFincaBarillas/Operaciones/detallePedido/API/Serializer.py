from rest_framework.serializers import ModelSerializer
from AppsFincaBarillas.Operaciones.detallePedido.models import DetallePedido

class DetallePedidoSerializer(ModelSerializer):
    class Meta:
        model = DetallePedido
        fields = ['PedidoId','ProductoId','Cantidad']
        # fields = '__all__'