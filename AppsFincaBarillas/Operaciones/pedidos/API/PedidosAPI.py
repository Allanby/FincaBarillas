from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny

from AppsFincaBarillas.Operaciones.pedidos.API.Serializer import PedidosSerializer
from AppsFincaBarillas.Operaciones.pedidos.models import Pedidos, pedidos

class PedidosViewSet(ViewSet):
    permission_classes = [IsAuthenticated] #[IsAdminOrReadOnly]
    queryset = Pedidos.objects.all()
    serializer = PedidosSerializer

    @action(methods=['get'], detail=False)
    def PedidosPendientes(self, request):
        try:

            # Filtrar los pedidos pendientes usando el campo 'estado'
            pedidos_pendientes = Pedidos.objects.filter(estado='Pendiente')

            # Si no se encuentran pedidos pendientes, devolver error
            if not pedidos_pendientes.exists():
                return Response(
                    status=status.HTTP_404_NOT_FOUND,
                    data={'error': 'No se encontraron pedidos pendientes'}
                )

            # Serializar los pedidos
            serializer = PedidosSerializer(pedidos_pendientes, many=True)


            # Retornar la respuesta con los datos serializados
            return Response(status=status.HTTP_200_OK, data={'PEDIDOS PENDIENTES': serializer.data})

        except Exception as e:
            # Manejar cualquier otro error inesperado
            return Response(
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                data={'error': 'Ocurrió un error inesperado.', 'detalle': str(e)}
            )

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

    def update(self, request, pk: int):
        pedidos = Pedidos.objects.get(pk=pk)
        serializer = PedidosSerializer(instance=pedidos, data=request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data= serializer.data)


    def delete(self, request, pk: int):
        pedidos = Pedidos.objects.get(pk=pk)
        serializer = PedidosSerializer(pedidos)
        pedidos.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)


    #Cambiar estado del pedido a "cancelado"

    @action(methods=['post'], detail=False)
    def CancelarPedido(self, request):
        id_pedido = request.data.get('idPedido')
        pedido = Pedidos.objects.filter(id_pedido=id_pedido).first()
        if pedido:
            pedido.Estado = 'Cancelado'
            pedido.save()
            return Response(status=status.HTTP_200_OK, data={'mensaje': 'Pedido cancelado'})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'mensaje': 'Pedido no encontrado'})

    #Filtrar pedidos realizados en noviembre

    @action(methods=['post'], detail=False)
    def FiltrarPedidosNoviembre(self, request):
        pedido = Pedidos.objects.filter(fecha_pedido=11)
        serializer = PedidosSerializer(pedido, many=True)
        data = {'mensaje': 'Pedidos realizados en noviembre', 'resultado': serializer.data}

        return Response(status=status.HTTP_200_OK, data=data)

    #Listar Pedidos de un Cliente Específico

    @action(methods=['get'], detail=False)
    def ListarPedidosPorCliente(self, request):
        cliente_id = request.query_params.get('ClienteId')
        pedidos = Pedidos().objects.filter(cliente=cliente_id)
        serializer = PedidosSerializer(pedidos, many=True)
        return Response(status=status.HTTP_200_OK, data={'resultado': serializer.data})


    # Reporte de pedidos por cliente:
    @action(methods=['get'], detail=False)
    def ReportePedidosPorCliente(self, request):
        cliente_id = request.query_params.get('cliente_id')
        pedidos = Pedidos.objects.filter(ClienteId=cliente_id)
        serializer = PedidosSerializer(pedidos, many=True)
        return Response(status=status.HTTP_200_OK, data={'reporte': serializer.data})









