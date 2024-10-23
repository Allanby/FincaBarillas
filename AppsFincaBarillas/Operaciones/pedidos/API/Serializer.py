from rest_framework.serializers import ModelSerializer
from AppsFincaBarillas.Operaciones.pedidos.models import Pedidos

class PedidosSerializer(ModelSerializer):
    class Meta:
        model = Pedidos
        fields = ['Id_Pedido','ClienteId','Fecha_Pedido', 'Estado']
        # fields = '__all__'