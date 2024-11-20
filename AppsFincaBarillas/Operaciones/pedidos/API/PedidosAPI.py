from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny

from AppsFincaBarillas.Operaciones.pedidos.API.Serializer import PedidosSerializer
from AppsFincaBarillas.Operaciones.pedidos.models import Pedidos, pedidos
from rest_framework.response import Response
from rest_framework import status
from collections import  namedtuple

# Estructura de respuesta estandarizada
ResponseData = namedtuple('ResponseData', ['Success', 'Status', 'Message', 'Record'])

def to_response(data: ResponseData):
    return {
        "success": data.Success,
        "status": data.Status,
        "message": data.Message,
        "record": data.Record,
    }

class PedidosViewSet(ViewSet):
    permission_classes = [IsAuthenticated] #[IsAdminOrReadOnly]
    queryset = Pedidos.objects.all()
    serializer = PedidosSerializer

    # Pedidos Pendientes
    @action(methods=['get'], detail=False)
    def PedidosPendientes(self, request):
        try:
            pedidos_pendientes = Pedidos.objects.filter(estado='Pendiente')

            if not pedidos_pendientes.exists():
                data = ResponseData(
                    Success=False,
                    Status=status.HTTP_404_NOT_FOUND,
                    Message="No se encontraron pedidos pendientes",
                    Record=None
                )
                return Response(status=status.HTTP_404_NOT_FOUND, data=to_response(data))

            serializer = PedidosSerializer(pedidos_pendientes, many=True)
            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message="Pedidos pendientes encontrados",
                Record=serializer.data
            )
            return Response(status=status.HTTP_200_OK, data=to_response(data))

        except Exception as e:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                Message="Ocurrió un error inesperado",
                Record={"detalle": str(e)}
            )
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=to_response(data))

    # Cancelar Pedido
    @action(methods=['post'], detail=False)
    def CancelarPedido(self, request):
        id_pedido = request.data.get('idPedido')
        pedido = Pedidos.objects.filter(id_pedido=id_pedido).first()

        if pedido:
            pedido.Estado = 'Cancelado'
            pedido.save()
            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message="Pedido cancelado correctamente",
                Record=None
            )
        else:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Pedido no encontrado",
                Record=None
            )
        return Response(status=data.Status, data=to_response(data))

    # Filtrar pedidos realizados en noviembre
    @action(methods=['post'], detail=False)
    def FiltrarPedidosNoviembre(self, request):
        try:
            pedidos = Pedidos.objects.filter(fecha_pedido__month=11)
            serializer = PedidosSerializer(pedidos, many=True)
            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message="Pedidos realizados en noviembre",
                Record=serializer.data
            )
            return Response(status=status.HTTP_200_OK, data=to_response(data))

        except Exception as e:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                Message="Ocurrió un error inesperado",
                Record={"detalle": str(e)}
            )
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR, data=to_response(data))

    # Listar Pedidos de un Cliente Específico
    @action(methods=['get'], detail=False)
    def ListarPedidosPorCliente(self, request):
        cliente_id = request.query_params.get('ClienteId')
        pedidos = Pedidos.objects.filter(ClienteId=cliente_id)

        if pedidos.exists():
            serializer = PedidosSerializer(pedidos, many=True)
            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message="Pedidos encontrados para el cliente especificado",
                Record=serializer.data
            )
        else:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message="No se encontraron pedidos para este cliente",
                Record=None
            )
        return Response(status=data.Status, data=to_response(data))

    # Reporte de pedidos por cliente
    @action(methods=['get'], detail=False)
    def ReportePedidosPorCliente(self, request):
        cliente_id = request.query_params.get('cliente_id')
        pedidos = Pedidos.objects.filter(ClienteId=cliente_id)

        if pedidos.exists():
            serializer = PedidosSerializer(pedidos, many=True)
            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message="Reporte generado exitosamente",
                Record=serializer.data
            )
        else:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message="No se encontraron pedidos para este cliente",
                Record=None
            )
        return Response(status=data.Status, data=to_response(data))








