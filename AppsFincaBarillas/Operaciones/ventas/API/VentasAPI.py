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

    #Actualizar el monto total de una venta existente:

    @action(methods=['post'], detail=False)
    def ActualizarMontoVenta(self, request):
        id_venta = request.data.get('id venta')
        nuevo_monto = request.data.get('monto total')
        venta = Venta.objects.filter(id_venta=id_venta).first()
        if venta:
            venta.monto_total = nuevo_monto
            venta.save()
            return Response(status=status.HTTP_200_OK, data={'mensaje': 'Monto actualizado'})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'mensaje': 'Venta no encontrada'})

    #Filtrar ventas con método de pago en efectivo y monto mayor a 30,000 córdobas

    @action(methods=['post'], detail=False)
    def FiltrarVentasEfectivo(self, request):
        ventas = Venta.objects.filter(MetodoPago='Efectivo', Monto__gt=30000)
        serializer = VentaSerializer(ventas, many=True)
        data = {'mensaje': 'Ventas en efectivo con monto superior a 30,000', 'resultado': serializer.data}

        return Response(status=status.HTTP_200_OK, data=data)








