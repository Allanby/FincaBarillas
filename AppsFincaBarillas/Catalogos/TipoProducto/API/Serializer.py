from rest_framework.serializers import ModelSerializer
from AppsFincaBarillas.Catalogos.TipoProducto.models import TipoProducto

class TipoProductoSerializer(ModelSerializer):
    class Meta:
        model = TipoProducto
        fields = ['Id_Tipo','Description']
        # fields = '__all__'