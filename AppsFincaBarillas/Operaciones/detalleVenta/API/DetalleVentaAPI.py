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




