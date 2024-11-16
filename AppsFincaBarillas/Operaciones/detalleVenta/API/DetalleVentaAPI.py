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

    def list(self, request):
        data = request
        serializer = DetalleVentaSerializer(DetalleVenta.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def retrieve(self, request, pk: int):
        serializer = DetalleVentaSerializer(DetalleVenta.objects.get(pk=pk))
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request):
        # Categoria.objects.create(Codigo=request.Post['Codigo'],Nombre=request.Post['Nombre'])
        serializer = DetalleVentaSerializer(data=request.Post)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def update(self, request, pk: int):
        detalleVenta = DetalleVenta.objects.get(pk=pk)
        serializer = DetalleVentaSerializer(instance=detalleVenta, data=request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data= serializer.data)


    def delete(self, request, pk: int):
        detalleVenta = DetalleVenta.objects.get(pk=pk)
        serializer = DetalleVentaSerializer(detalleVenta)
        detalleVenta.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

    #Actualizar detalle venta
    @action(methods=['put'], detail=False)
    def ActualizarDetalleVenta(self, request):
        detalle_id = request.data.get('DetalleId')
        nueva_cantidad = request.data.get('Cantidad')
        nuevo_precio = request.data.get('PrecioProducto')

        detalle_venta = DetalleVenta.objects.filter(id=detalle_id).first()
        if detalle_venta:
            if nueva_cantidad is not None:
                detalle_venta.cantidadProducto = nueva_cantidad
            if nuevo_precio is not None:
                detalle_venta.PrecioProducto = nuevo_precio
            detalle_venta.save()
            return Response(status=status.HTTP_200_OK, data={'mensaje': 'Detalle de venta actualizado'})
        return Response(status=status.HTTP_404_NOT_FOUND, data={'mensaje': 'Detalle de venta no encontrado'})

    #Reporte de productos más vendidos:
    @action(methods=['get'], detail=False)
    def ReporteProductosMasVendidos(self, request):
        productos_mas_vendidos = DetalleVenta.objects.values('ProductoID').annotate(
            total_vendido=sum('cantidadProducto')).order_by('-total_vendido')
        return Response(status=status.HTTP_200_OK, data={'reporte': productos_mas_vendidos})

    #Obtener total de productos vendidos en una venta específica:

    @action(methods=['get'], detail=True)
    def TotalProductosVendidos(self, request, pk=None):
        detalles = DetalleVenta.objects.filter(VentaI=pk)
        total = detalles.aggregate(sum('cantidadProducto'))['cantidadProducto__sum']
        return Response(status=status.HTTP_200_OK, data={'total_productos': total})

    #Filtrar detalles de venta por precio mínimo:
    @action(methods=['get'], detail=False)
    def FiltrarPorPrecioMinimo(self, request):
        precio_min = request.query_params.get('precio_min', 0)
        detalles = DetalleVenta.objects.filter(PrecioProducto__gte=precio_min)
        serializer = DetalleVentaSerializer(detalles, many=True)
        return Response(status=status.HTTP_200_OK, data={'resultado': serializer.data})








