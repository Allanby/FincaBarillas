from rest_framework.serializers import ModelSerializer
from AppsFincaBarillas.Operaciones.producciones.models import Producciones

class ProduccionesSerializer(ModelSerializer):
    class Meta:
        model =  Producciones
        fields = ['Id_produccion','codigo_produccion','producto','calidad_cosecha', 'fecha_produccion', 'cantidad_producida', 'lapso_produccion']
        # fields = '__all__'