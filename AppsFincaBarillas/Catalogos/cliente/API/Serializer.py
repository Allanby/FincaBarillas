from rest_framework.serializers import ModelSerializer
from AppsFincaBarillas.Catalogos.cliente.models import Cliente

class ClienteSerializer(ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id','codigo','nombres', 'apellidos', 'telefono', 'direccion', 'estado']
        # fields = '__all__'