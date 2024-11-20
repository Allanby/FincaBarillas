from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from AppsFincaBarillas.Operaciones.detalleVenta.API.Permission import IsAdminOrReadOnly
#IsAuthenticated: solo usuarios logeados en el panel adminitrativo
#IsAdminUser: solo los usuarios administradores podran acceder
#IsAuthenticatedOrReadOnly: solo los usuarios autenticado podran hacer CDU el resto solo lectura
#Existen otros y crear nuestros propios permisos
#AllowAny: para indicar que es un endpoit libre sin aunteticacion

from AppsFincaBarillas.Operaciones.detalleVenta.API.Serializer import DetalleVentaSerializer
from AppsFincaBarillas.Operaciones.detalleVenta.models import DetalleVenta
from AppsFincaBarillas.Operaciones.detalleVenta.API.Permission import IsAdminOrReadOnly

class DetalleVentaViewSet(ViewSet):
    permission_classes = [IsAuthenticated] #[IsAdminOrReadOnly]
    queryset = DetalleVenta.objects.all()
    serializer = DetalleVentaSerializer

    # Listar todos los detalles de venta
    def list(self, request):
        detalles_venta = DetalleVenta.objects.all()
        serializer = DetalleVentaSerializer(detalles_venta, many=True)
        return Response({
            "success": True,
            "status": status.HTTP_200_OK,
            "message": "Listado de detalles de venta",
            "record": serializer.data
        }, status=status.HTTP_200_OK)

    # Obtener un detalle de venta específico
    def retrieve(self, request, pk: int):
        try:
            detalle_venta = DetalleVenta.objects.get(pk=pk)
            serializer = DetalleVentaSerializer(detalle_venta)
            return Response({
                "success": True,
                "status": status.HTTP_200_OK,
                "message": "Detalle de venta encontrado",
                "record": serializer.data
            }, status=status.HTTP_200_OK)
        except DetalleVenta.DoesNotExist:
            return Response({
                "success": False,
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Detalle de venta no encontrado",
                "record": []
            }, status=status.HTTP_404_NOT_FOUND)

    # Crear un nuevo detalle de venta
    def create(self, request):
        serializer = DetalleVentaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "success": True,
            "status": status.HTTP_200_OK,
            "message": "Detalle de venta creado exitosamente",
            "record": serializer.data
        }, status=status.HTTP_200_OK)

    # Actualizar un detalle de venta existente
    def update(self, request, pk: int):
        try:
            detalle_venta = DetalleVenta.objects.get(pk=pk)
            serializer = DetalleVentaSerializer(instance=detalle_venta, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "success": True,
                "status": status.HTTP_200_OK,
                "message": "Detalle de venta actualizado exitosamente",
                "record": serializer.data
            }, status=status.HTTP_200_OK)
        except DetalleVenta.DoesNotExist:
            return Response({
                "success": False,
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Detalle de venta no encontrado",
                "record": []
            }, status=status.HTTP_404_NOT_FOUND)

    # Eliminar un detalle de venta
    def delete(self, request, pk: int):
        try:
            detalle_venta = DetalleVenta.objects.get(pk=pk)
            detalle_venta.delete()
            return Response({
                "success": True,
                "status": status.HTTP_204_NO_CONTENT,
                "message": "Detalle de venta eliminado exitosamente",
                "record": []
            }, status=status.HTTP_204_NO_CONTENT)
        except DetalleVenta.DoesNotExist:
            return Response({
                "success": False,
                "status": status.HTTP_404_NOT_FOUND,
                "message": "Detalle de venta no encontrado",
                "record": []
            }, status=status.HTTP_404_NOT_FOUND)

    # Actualizar la cantidad y el precio de un detalle de venta
    @action(methods=['put'], detail=False)
    def ActualizarDetalleVenta(self, request):
        detalle_id = request.data.get('DetalleId')
        nueva_cantidad = request.data.get('Cantidad')
        nuevo_precio = request.data.get('PrecioProducto')

        detalle_venta = DetalleVenta.objects.filter(Id_DetalleVenta=detalle_id).first()
        if detalle_venta:
            if nueva_cantidad is not None:
                detalle_venta.cantidad_producto = nueva_cantidad
            if nuevo_precio is not None:
                detalle_venta.precio_producto = nuevo_precio
            detalle_venta.save()
            return Response({
                "success": True,
                "status": status.HTTP_200_OK,
                "message": "Detalle de venta actualizado exitosamente"
            }, status=status.HTTP_200_OK)
        return Response({
            "success": False,
            "status": status.HTTP_404_NOT_FOUND,
            "message": "Detalle de venta no encontrado"
        }, status=status.HTTP_404_NOT_FOUND)

    # Reporte de productos más vendidos
    @action(methods=['get'], detail=False)
    def ReporteProductosMasVendidos(self, request):
        productos_mas_vendidos = DetalleVenta.objects.values('producto__nombre').annotate(
            total_vendido=models.Sum('cantidad_producto')
        ).order_by('-total_vendido')
        return Response({
            "success": True,
            "status": status.HTTP_200_OK,
            "message": "Reporte de productos más vendidos",
            "record": productos_mas_vendidos
        }, status=status.HTTP_200_OK)

    # Obtener el total de productos vendidos en una venta específica
    @action(methods=['get'], detail=True)
    def TotalProductosVendidos(self, request, pk=None):
        detalles = DetalleVenta.objects.filter(venta_id=pk)
        total = detalles.aggregate(total_vendido=models.Sum('cantidad_producto'))['total_vendido']
        return Response({
            "success": True,
            "status": status.HTTP_200_OK,
            "message": "Total de productos vendidos",
            "record": {'total_productos': total}
        }, status=status.HTTP_200_OK)

    # Filtrar detalles de venta por precio mínimo
    @action(methods=['get'], detail=False)
    def FiltrarPorPrecioMinimo(self, request):
        precio_min = request.query_params.get('precio_min', 0)
        detalles = DetalleVenta.objects.filter(precio_producto__gte=precio_min)
        serializer = DetalleVentaSerializer(detalles, many=True)
        return Response({
            "success": True,
            "status": status.HTTP_200_OK,
            "message": "Detalles de venta filtrados por precio mínimo",
            "record": serializer.data
        }, status=status.HTTP_200_OK)







