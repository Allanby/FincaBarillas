from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from AppsFincaBarillas.Catalogos.TipoProducto.API.Serializer import TipoProductoSerializer
from AppsFincaBarillas.Catalogos.TipoProducto.models import TipoProducto

class TipoProductoViewSet(ViewSet):
    permission_classes = [IsAuthenticated] #[IsAdminOrReadOnly]
    queryset = TipoProducto.objects.all()
    serializer = TipoProductoSerializer

    # Listar todos los tipos de producto
    def list(self, request):
        serializer = TipoProductoSerializer(TipoProducto.objects.all(), many=True)
        return Response({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Listado de tipos de producto',
            'record': serializer.data
        }, status=status.HTTP_200_OK)

    # Obtener un tipo de producto específico
    def retrieve(self, request, pk: int):
        try:
            tipo_producto = TipoProducto.objects.get(pk=pk)
            serializer = TipoProductoSerializer(tipo_producto)
            return Response({
                'success': True,
                'status': status.HTTP_200_OK,
                'message': 'Tipo de producto encontrado',
                'record': serializer.data
            }, status=status.HTTP_200_OK)
        except TipoProducto.DoesNotExist:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Tipo de producto no encontrado',
                'record': []
            }, status=status.HTTP_404_NOT_FOUND)

    # Crear un nuevo tipo de producto
    def create(self, request):
        serializer = TipoProductoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'success': True,
                'status': status.HTTP_201_CREATED,
                'message': 'Tipo de producto creado exitosamente',
                'record': serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            'success': False,
            'status': status.HTTP_400_BAD_REQUEST,
            'message': 'Error al crear el tipo de producto',
            'record': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    # Actualizar un tipo de producto existente
    def update(self, request, pk: int):
        try:
            tipo_producto = TipoProducto.objects.get(pk=pk)
            serializer = TipoProductoSerializer(instance=tipo_producto, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'success': True,
                    'status': status.HTTP_200_OK,
                    'message': 'Tipo de producto actualizado exitosamente',
                    'record': serializer.data
                }, status=status.HTTP_200_OK)
        except TipoProducto.DoesNotExist:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Tipo de producto no encontrado',
                'record': []
            }, status=status.HTTP_404_NOT_FOUND)

    # Eliminar un tipo de producto
    def delete(self, request, pk: int):
        try:
            tipo_producto = TipoProducto.objects.get(pk=pk)
            tipo_producto.delete()
            return Response({
                'success': True,
                'status': status.HTTP_204_NO_CONTENT,
                'message': 'Tipo de producto eliminado exitosamente',
                'record': []
            }, status=status.HTTP_204_NO_CONTENT)
        except TipoProducto.DoesNotExist:
            return Response({
                'success': False,
                'status': status.HTTP_404_NOT_FOUND,
                'message': 'Tipo de producto no encontrado',
                'record': []
            }, status=status.HTTP_404_NOT_FOUND)

    # Filtrar por descripción que contenga "buena calidad"
    @action(methods=['post'], detail=False)
    def FiltrarPorCalidad(self, request):
        calidad = "buena calidad"
        tipos_producto = TipoProducto.objects.filter(description__icontains=calidad)
        serializer = TipoProductoSerializer(tipos_producto, many=True)
        return Response({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Tipos de producto con buena calidad',
            'record': serializer.data
        }, status=status.HTTP_200_OK)

    # Listar tipos de producto por popularidad (basado en las ventas)
    @action(methods=['get'], detail=False)
    def ListarPorPopularidad(self, request):
        tipos = TipoProducto.objects.annotate(num_ventas=Count('productos__detalle_venta')).order_by('-num_ventas')
        serializer = TipoProductoSerializer(tipos, many=True)
        return Response({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Tipos de producto por popularidad',
            'record': serializer.data
        }, status=status.HTTP_200_OK)

    # Reporte de tipos de producto por cantidad de productos
    @action(methods=['get'], detail=False)
    def ReporteTiposProductoPorCantidad(self, request):
        tipos_producto_cantidad = TipoProducto.objects.values('description').annotate(
            cantidad_productos=Count('id')
        ).order_by('-cantidad_productos')

        data = [{'tipo_producto': t['description'], 'cantidad_productos': t['cantidad_productos']} for t in
                tipos_producto_cantidad]
        return Response({
            'success': True,
            'status': status.HTTP_200_OK,
            'message': 'Reporte de tipos de producto por cantidad',
            'record': data
        }, status=status.HTTP_200_OK)







