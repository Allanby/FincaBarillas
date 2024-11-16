from django.db.models.functions import TruncMonth
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from AppsFincaBarillas.Operaciones.ventas.API.Permission import IsAdminOrReadOnly
#IsAuthenticated: solo usuarios logeados en el panel adminitrativo
#IsAdminUser: solo los usuarios administradores podran acceder
#IsAuthenticatedOrReadOnly: solo los usuarios autenticado podran hacer CDU el resto solo lectura
#Existen otros y crear nuestros propios permisos
#AllowAny: para indicar que es un endpoit libre sin aunteticacion

from AppsFincaBarillas.Operaciones.ventas.API.Serializer import VentaSerializer
from AppsFincaBarillas.Operaciones.ventas.models import Venta
from AppsFincaBarillas.Operaciones.ventas.API.Permission import IsAdminOrReadOnly

class VentaViewSet(ViewSet):
    permission_classes = [IsAuthenticated] #[IsAdminOrReadOnly]
    queryset = Venta.objects.all()
    serializer = VentaSerializer

    def list(self, request):
        data = request
        serializer = VentaSerializer(Venta.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def retrieve(self, request, pk: int):
        serializer = VentaSerializer(Venta.objects.get(pk=pk))
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request):
        # Categoria.objects.create(Codigo=request.Post['Codigo'],Nombre=request.Post['Nombre'])
        serializer = VentaSerializer(data=request.Post)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def update(self, request, pk: int):
        ventas = Venta.objects.get(pk=pk)
        serializer = VentaSerializer(instance=ventas, data=request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data= serializer.data)


    def delete(self, request, pk: int):
        ventas = Venta.objects.get(pk=pk)
        serializer = VentaSerializer(ventas)
        ventas.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)


    #Buscar ventas por método de pago:

    @action(methods=['get'], detail=False)
    def BuscarPorMetodoPago(self, request):
        metodo_pago = request.query_params.get('metodo')
        ventas = Venta.objects.filter(metodoPago__icontains=metodo_pago)
        serializer = VentaSerializer(ventas, many=True)
        return Response(status=status.HTTP_200_OK, data={'resultado': serializer.data})

    #Filtrar ventas con metodo de pago en efectivo y monto mayor a 30, 000 cordobas
    @action(methods=['post'], detail=False)
    def FiltrarVentasEfectivo(self, request):
        ventas = Venta.objects.filter(MetodoPago='Efectivo', Monto__gt=30000)
        serializer = VentaSerializer(ventas, many=True)
        data = {'mensaje': 'Ventas en efectivo con monto superior a 30,000', 'resultado': serializer.data}

        return Response(status=status.HTTP_200_OK, data=data)

    #Reporte de ventas por mes:
    @action(methods=['get'], detail=False)
    def ReporteVentasPorMes(self, request):
        ventas_mes = Venta.objects.annotate(mes=TruncMonth('fechaventa')).values('mes').annotate(
            total=sum('monto total')).order_by('mes')
        return Response(status=status.HTTP_200_OK, data={'reporte': ventas_mes})

    # Reporte de ventas por método de pago:
    @action(methods=['get'], detail=False)
    def ReporteVentasPorMetodoPago(self, request):
        ventas_metodo = Venta.objects.values('metodoPago').annotate(total_ventas=sum('monto total'))
        return Response(status=status.HTTP_200_OK, data={'reporte': ventas_metodo})












