from django.db.models.functions import TruncMonth
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models.functions import TruncMonth
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny

from AppsFincaBarillas.Operaciones.ventas.API.Serializer import VentaSerializer
from AppsFincaBarillas.Operaciones.ventas.models import Venta

class VentaViewSet(ViewSet):
    permission_classes = [IsAuthenticated] #[IsAdminOrReadOnly]
    queryset = Venta.objects.all()
    serializer = VentaSerializer

    def list(self, request):
        ventas = Venta.objects.all()
        serializer = VentaSerializer(ventas, many=True)
        return Response({
            "success": True,
            "status": HTTP_200_OK,
            "message": "Listado de ventas",
            "record": serializer.data
        }, status=HTTP_200_OK)

    def retrieve(self, request, pk: int):
        try:
            venta = Venta.objects.get(pk=pk)
            serializer = VentaSerializer(venta)
            return Response({
                "success": True,
                "status": HTTP_200_OK,
                "message": "Detalle de la venta",
                "record": serializer.data
            }, status=HTTP_200_OK)
        except Venta.DoesNotExist:
            return Response({
                "success": False,
                "status": HTTP_404_NOT_FOUND,
                "message": "Venta no encontrada",
                "record": []
            }, status=HTTP_404_NOT_FOUND)

    def create(self, request):
        serializer = VentaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "success": True,
            "status": HTTP_200_OK,
            "message": "Venta creada exitosamente",
            "record": serializer.data
        }, status=HTTP_200_OK)

    def update(self, request, pk: int):
        try:
            venta = Venta.objects.get(pk=pk)
            serializer = VentaSerializer(instance=venta, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "success": True,
                "status": HTTP_200_OK,
                "message": "Venta actualizada exitosamente",
                "record": serializer.data
            }, status=HTTP_200_OK)
        except Venta.DoesNotExist:
            return Response({
                "success": False,
                "status": HTTP_404_NOT_FOUND,
                "message": "Venta no encontrada",
                "record": []
            }, status=HTTP_404_NOT_FOUND)

    def delete(self, request, pk: int):
        try:
            venta = Venta.objects.get(pk=pk)
            venta.delete()
            return Response({
                "success": True,
                "status": HTTP_204_NO_CONTENT,
                "message": "Venta eliminada exitosamente",
                "record": []
            }, status=HTTP_204_NO_CONTENT)
        except Venta.DoesNotExist:
            return Response({
                "success": False,
                "status": HTTP_404_NOT_FOUND,
                "message": "Venta no encontrada",
                "record": []
            }, status=HTTP_404_NOT_FOUND)

    # Acción de filtrado de ventas por método de pago:
    @action(methods=['get'], detail=False)
    def BuscarPorMetodoPago(self, request):
        metodo_pago = request.query_params.get('metodo')
        ventas = Venta.objects.filter(metodo_pago__icontains=metodo_pago)  # Cambiado metodoPago a metodo_pago
        serializer = VentaSerializer(ventas, many=True)
        return Response({
            "success": True,
            "status": HTTP_200_OK,
            "message": f"Ventas con método de pago '{metodo_pago}'",
            "record": serializer.data
        }, status=HTTP_200_OK)

    # Acción de filtrado de ventas por efectivo y monto:
    @action(methods=['POST'], detail=False)
    def FiltrarVentasEfectivo(self, request):
        metodo_pago = request.data.get('metodo_pago', 'Efectivo')  # Cambiado metodoPago a metodo_pago
        monto_total = request.data.get('monto_total', 30000)  # Cambiado monto total a monto_total
        ventas = Venta.objects.filter(metodo_pago=metodo_pago, monto_total__gt=monto_total)  # Cambiado monto total
        if not ventas.exists():
            return Response({
                "success": False,
                "status": HTTP_404_NOT_FOUND,
                "message": "No se encontraron ventas con los criterios especificados",
                "record": []
            }, status=HTTP_404_NOT_FOUND)
        serializer = VentaSerializer(ventas, many=True)
        return Response({
            "success": True,
            "status": HTTP_200_OK,
            "message": f"Ventas con método de pago {metodo_pago} y monto superior a {monto_total}",
            "record": serializer.data
        }, status=HTTP_200_OK)

    # Acción de reporte de ventas por mes:
    @action(methods=['GET'], detail=False)
    def ReporteVentasPorMes(self, request):
        ventas_mes = (
            Venta.objects.annotate(mes=TruncMonth('fecha_venta'))  # Cambiado fechaventa a fecha_venta
            .values('mes')
            .annotate(total=Sum('monto_total'))  # Cambiado monto total a monto_total
            .order_by('mes')
        )
        return Response({
            "success": True,
            "status": HTTP_200_OK,
            "message": "Reporte de ventas por mes",
            "record": list(ventas_mes)
        }, status=HTTP_200_OK)
