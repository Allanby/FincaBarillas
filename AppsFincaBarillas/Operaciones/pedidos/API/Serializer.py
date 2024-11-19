from rest_framework.serializers import ModelSerializer
from AppsFincaBarillas.Operaciones.pedidos.models import Pedidos

class PedidosSerializer(ModelSerializer):
    class Meta:
        model = Pedidos
        fields = ['id_pedido','cliente','fecha_pedido', 'estado']
        # fields = '__all__'