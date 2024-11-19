from rest_framework.serializers import ModelSerializer
from AppsFincaBarillas.Operaciones.ventas.models import Venta

class VentaSerializer(ModelSerializer):
    class Meta:
        model = Venta
        fields = ['id_venta','cliente','numero_venta','metodo_pago', 'fecha_venta','monto_total']
        # fields = '__all__'