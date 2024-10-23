from rest_framework.serializers import ModelSerializer
from AppsFincaBarillas.Catalogos.producto.models import producto

class ProductoSerializer(ModelSerializer):
    class Meta:
        model = producto
        fields = ['Id_Producto','Codigo_Cultivo','Nombre', 'TipoId', 'Fecha_Siembra', 'Estado']
        # fields = '__all__'