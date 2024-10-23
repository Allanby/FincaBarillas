from rest_framework.serializers import ModelSerializer
from AppsFincaBarillas.Operaciones.producciones.models import Producciones

class ProduccionesSerializer(ModelSerializer):
    class Meta:
        model =  Producciones
        fields = ['Id_Produccion','ProductoId','Codigo_Produccion','Calidad_Cosecha', 'Fecha_Produccion', 'Cantidad_Producida', 'Labso_Produccion']
        # fields = '__all__'