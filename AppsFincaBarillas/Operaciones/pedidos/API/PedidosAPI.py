from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from AppsFincaBarillas.Operaciones.pedidos.API.Permission import IsAdminOrReadOnly
#IsAuthenticated: solo usuarios logeados en el panel adminitrativo
#IsAdminUser: solo los usuarios administradores podran acceder
#IsAuthenticatedOrReadOnly: solo los usuarios autenticado podran hacer CDU el resto solo lectura
#Existen otros y crear nuestros propios permisos
#AllowAny: para indicar que es un endpoit libre sin aunteticacion

from AppsFincaBarillas.Operaciones.pedidos.API.Serializer import PedidosSerializer
from AppsFincaBarillas.Operaciones.pedidos.models import Pedidos
from AppsFincaBarillas.Operaciones.pedidos.API.Permission import IsAdminOrReadOnly

class PedidosViewSet(ViewSet):
    permission_classes = [IsAuthenticated] #[IsAdminOrReadOnly]
    queryset = Pedidos.objects.all()
    serializer = PedidosSerializer

    def list(self, request):
        data = request
        serializer = PedidosSerializer(Pedidos.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def retrieve(self, request, pk: int):
        serializer = PedidosSerializer(Pedidos.objects.get(pk=pk))
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request):
        # Categoria.objects.create(Codigo=request.Post['Codigo'],Nombre=request.Post['Nombre'])
        serializer = PedidosSerializer(data=request.Post)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)


    #Cambiar estado del pedido a "cancelado"

    @action(methods=['post'], detail=False)
    def CancelarPedido(self, request):
        id_pedido = request.data.get('idPedido')
        pedido = Pedidos.objects.filter(idPedido=id_pedido).first()
        if pedido:
            pedido.Estado = 'Cancelado'
            pedido.save()
            return Response(status=status.HTTP_200_OK, data={'mensaje': 'Pedido cancelado'})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'mensaje': 'Pedido no encontrado'})

    #Filtrar pedidos realizados en noviembre

    @action(methods=['post'], detail=False)
    def FiltrarPedidosNoviembre(self, request):
        pedido = Pedidos.objects.filter(Fecha__month=11)
        serializer = PedidosSerializer(pedido, many=True)
        data = {'mensaje': 'Pedidos realizados en noviembre', 'resultado': serializer.data}

        return Response(status=status.HTTP_200_OK, data=data)




