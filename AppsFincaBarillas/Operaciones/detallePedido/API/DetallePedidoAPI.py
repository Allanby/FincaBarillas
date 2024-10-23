from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from AppsFincaBarillas.Operaciones.detallePedido.API.Permission import IsAdminOrReadOnly
#IsAuthenticated: solo usuarios logeados en el panel adminitrativo
#IsAdminUser: solo los usuarios administradores podran acceder
#IsAuthenticatedOrReadOnly: solo los usuarios autenticado podran hacer CDU el resto solo lectura
#Existen otros y crear nuestros propios permisos
#AllowAny: para indicar que es un endpoit libre sin aunteticacion

from AppsFincaBarillas.Operaciones.detallePedido.API.Serializer import DetallePedidoSerializer
from AppsFincaBarillas.Operaciones.detallePedido.models import DetallePedido
from AppsFincaBarillas.Operaciones.detallePedido.API.Permission import IsAdminOrReadOnly

class DetallePedidoViewSet(ViewSet):
    permission_classes = [IsAuthenticated] #[IsAdminOrReadOnly]
    queryset = DetallePedido.objects.all()
    serializer = DetallePedidoSerializer

    def list(self, request):
        data = request
        serializer = DetallePedidoSerializer(DetallePedido.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def retrieve(self, request, pk: int):
        serializer = DetallePedidoSerializer(DetallePedido.objects.get(pk=pk))
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request):
        # Categoria.objects.create(Codigo=request.Post['Codigo'],Nombre=request.Post['Nombre'])
        serializer = DetallePedidoSerializer(data=request.Post)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    #Actualizar la cantidad de productos en un detalle de pedido

    @action(methods=['post'], detail=False)
    def ActualizarCantidadProducto(self, request):
        pedido_id = request.data.get('PedidoId')
        producto_id = request.data.get('ProductoID')
        nueva_cantidad = request.data.get('Cantidad')
        detalle_pedido = DetallePedido.objects.filter(PedidoId=pedido_id, ProductoID=producto_id).first()
        if detalle_pedido:
            detalle_pedido.Cantidad = nueva_cantidad
            detalle_pedido.save()
            return Response(status=status.HTTP_200_OK, data={'mensaje': 'Cantidad actualizada'})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'mensaje': 'Detalle de pedido no encontrado'})





