from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from AppsFincaBarillas.Catalogos.TipoProducto.API.Permission import IsAdminOrReadOnly
#IsAuthenticated: solo usuarios logeados en el panel adminitrativo
#IsAdminUser: solo los usuarios administradores podran acceder
#IsAuthenticatedOrReadOnly: solo los usuarios autenticado podran hacer CDU el resto solo lectura
#Existen otros y crear nuestros propios permisos
#AllowAny: para indicar que es un endpoit libre sin aunteticacion

from AppsFincaBarillas.Catalogos.TipoProducto.API.Serializer import TipoProductoSerializer
from AppsFincaBarillas.Catalogos.TipoProducto.models import TipoProducto
from AppsFincaBarillas.Catalogos.TipoProducto.API.Permission import IsAdminOrReadOnly

class TipoProductoViewSet(ViewSet):
    permission_classes = [IsAuthenticated] #[IsAdminOrReadOnly]
    queryset = TipoProducto.objects.all()
    serializer = TipoProductoSerializer

    def list(self, request):
        data = request
        serializer = TipoProductoSerializer(TipoProducto.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def retrieve(self, request, pk: int):
        serializer = TipoProductoSerializer(TipoProducto.objects.get(pk=pk))
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request):
        # TipoProducto.objects.create(Codigo=request.Post['Codigo'],Nombre=request.Post['Nombre'])
        serializer = TipoProductoSerializer(data=request.Post)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    #Filtrar por descripción que contenga "buena calidad"

    @action(methods=['post'], detail=False)
    def FiltrarPorCalidad(self, request):
        calidad = "buena calidad"
        tipos_producto = TipoProducto.objects.filter(Descripcion__icontains=calidad)
        serializer = TipoProductoSerializer(tipos_producto, many=True)
        data = {'mensaje': 'Tipos de producto con buena calidad', 'resultado': serializer.data}

        return Response(status=status.HTTP_200_OK, data=data) 





