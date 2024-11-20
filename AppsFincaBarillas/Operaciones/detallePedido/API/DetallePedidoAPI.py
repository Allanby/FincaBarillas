from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from django.db.models import Sum
from AppsFincaBarillas.Operaciones.detallePedido import models
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from AppsFincaBarillas.Operaciones.detallePedido.API.Serializer import DetallePedidoSerializer
from AppsFincaBarillas.Operaciones.detallePedido.models import DetallePedido
from AppsFincaBarillas.Operaciones.detallePedido.API.Permission import IsAdminOrReadOnly

class DetallePedidoViewSet(ViewSet):
    permission_classes = [IsAuthenticated] #[IsAdminOrReadOnly]
    queryset = DetallePedido.objects.all()
    serializer = DetallePedidoSerializer

    # Listar todos los detalles de pedido
    def list(self, request):
        serializer = DetallePedidoSerializer(DetallePedido.objects.all(), many=True)
        return Response({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Listado de detalles de pedido',
            'record': serializer.data
        }, status=status.HTTP_200_OK)

    # Obtener un detalle de pedido específico
    def retrieve(self, request, pk: int):
        try:
            detalle_pedido = DetallePedido.objects.get(pk=pk)
            serializer = DetallePedidoSerializer(detalle_pedido)
            return Response({
                'success': True,
                'status': status.HTTP_200_OK,
                'message': 'Detalle de pedido encontrado',
                'record': serializer.data
            }, status=status.HTTP_200_OK)
        except DetallePedido.DoesNotExist:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Detalle de pedido no encontrado',
                'record': []
            }, status=status.HTTP_404_NOT_FOUND)

    # Crear un nuevo detalle de pedido
    def create(self, request):
        serializer = DetallePedidoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'status': status.HTTP_201_CREATED,
                'message': 'Detalle de pedido creado exitosamente',
                'record': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Error al crear el detalle de pedido',
            'record': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # Actualizar un detalle de pedido existente
    def update(self, request, pk: int):
        try:
            detalle_pedido = DetallePedido.objects.get(pk=pk)
            serializer = DetallePedidoSerializer(instance=detalle_pedido, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'status': status.HTTP_200_OK,
                    'message': 'Detalle de pedido actualizado exitosamente',
                    'record': serializer.data
                }, status=status.HTTP_200_OK)
        except DetallePedido.DoesNotExist:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Detalle de pedido no encontrado',
                'record': []
            }, status=status.HTTP_404_NOT_FOUND)

    # Eliminar un detalle de pedido
    def delete(self, request, pk: int):
        try:
            detalle_pedido = DetallePedido.objects.get(pk=pk)
            detalle_pedido.delete()
            return Response({
                'success': True,
                'status': status.HTTP_204_NO_CONTENT,
                'message': 'Detalle de pedido eliminado exitosamente',
                'record': []
            }, status=status.HTTP_204_NO_CONTENT)
        except DetallePedido.DoesNotExist:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Detalle de pedido no encontrado',
                'record': []
            }, status=status.HTTP_404_NOT_FOUND)

    # Actualizar la cantidad de productos en un detalle de pedido
    @action(methods=['post'], detail=False)
    def ActualizarCantidadProducto(self, request):
        pedido_id = request.data.get('PedidoId')
        producto_id = request.data.get('ProductoID')
        nueva_cantidad = request.data.get('Cantidad')

        detalle_pedido = DetallePedido.objects.filter(pedido_id=pedido_id, producto_id=producto_id).first()

        if detalle_pedido:
            detalle_pedido.cantidad = nueva_cantidad
            detalle_pedido.save()
            return Response({
                'success': True,
                'status': status.HTTP_200_OK,
                'message': 'Cantidad actualizada'
            }, status=status.HTTP_200_OK)

        return Response({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Detalle de pedido no encontrado'
        }, status=status.HTTP_400_BAD_REQUEST)

    # Obtener total de productos vendidos en un pedido específico
    @action(methods=['get'], detail=True)
    def TotalProductosVendidos(self, request, pk=None):
        detalles = DetallePedido.objects.filter(pedido_id=pk)
        total = detalles.aggregate(total_vendido=Sum('cantidad'))['total_vendido']
        return Response({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Total de productos vendidos en el pedido',
            'record': {'total_productos': total}
        }, status=status.HTTP_200_OK)




