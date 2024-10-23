from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from AppsFincaBarillas.Operaciones.producciones.API.Permission import IsAdminOrReadOnly
#IsAuthenticated: solo usuarios logeados en el panel adminitrativo
#IsAdminUser: solo los usuarios administradores podran acceder
#IsAuthenticatedOrReadOnly: solo los usuarios autenticado podran hacer CDU el resto solo lectura
#Existen otros y crear nuestros propios permisos
#AllowAny: para indicar que es un endpoit libre sin aunteticacion

from AppsFincaBarillas.Operaciones.producciones.API.Serializer import ProduccionesSerializer
from AppsFincaBarillas.Operaciones.producciones.models import Producciones
from AppsFincaBarillas.Operaciones.producciones.API.Permission import IsAdminOrReadOnly

class ProduccionesViewSet(ViewSet):
    permission_classes = [IsAuthenticated] #[IsAdminOrReadOnly]
    queryset = Producciones.objects.all()
    serializer = ProduccionesSerializer

    def list(self, request):
        data = request
        serializer = ProduccionesSerializer(Producciones.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def retrieve(self, request, pk: int):
        serializer = ProduccionesSerializer(Producciones.objects.get(pk=pk))
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request):
        # Categoria.objects.create(Codigo=request.Post['Codigo'],Nombre=request.Post['Nombre'])
        serializer = ProduccionesSerializer(data=request.Post)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)


    #Registrar una producción con calidad "excelente"

    @action(methods=['post'], detail=False)
    def RegistrarProduccionExcelente(self, request):
        data_produccion = request.data
        data_produccion['CalidadCosecha'] = 'Excelente'
        serializer = ProduccionesSerializer(data=data_produccion)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data={'mensaje': 'Producción registrada con calidad excelente'})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'mensaje': 'Datos inválidos'})



