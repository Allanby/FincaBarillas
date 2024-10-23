from rest_framework.serializers import ModelSerializer
from AppsFincaBarillas.Operaciones.ventas.models import Venta

class VentaSerializer(ModelSerializer):
    class Meta:
        model = Venta
        fields = ['Id_Venta','ClienteId','N_Venta','Metodo_Pago', 'Fecha_Venta', 'Monto_Total']
        # fields = '__all__'