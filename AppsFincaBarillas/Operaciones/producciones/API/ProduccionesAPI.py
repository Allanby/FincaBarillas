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

    def update(self, request, pk: int):
        producciones = Producciones.objects.get(pk=pk)
        serializer = ProduccionesSerializer(instance=producciones, data=request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data= serializer.data)


    def delete(self, request, pk: int):
        producciones = Producciones.objects.get(pk=pk)
        serializer = ProduccionesSerializer(producciones)
        producciones.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

    #Filtrar Producciones por Fecha de Producción
    @action(methods=['get'], detail=False)
    def FiltrarProduccionesPorFecha(self, request):
        fecha_inicio = request.query_params.get('FechaInicio')
        fecha_fin = request.query_params.get('FechaFin')

        if not fecha_inicio or not fecha_fin:
            return Response(status=status.HTTP_400_BAD_REQUEST,
            data={'mensaje': 'FechaInicio y FechaFin son requeridos'})

        producciones = Producciones.objects.filter(FechaProduccion__range=[fecha_inicio, fecha_fin])
        serializer = ProduccionesSerializer(producciones, many=True)
        return Response(status=status.HTTP_200_OK, data={'resultado': serializer.data})

    #Obtener la producción más reciente:
    @action(methods=['get'], detail=False)
    def ProduccionMasReciente(self, request):
        produccion = Producciones.objects.latest('FechaProduccion')
        serializer = ProduccionesSerializer(produccion)
        return Response(status=status.HTTP_200_OK, data={'resultado': serializer.data})

    #Reporte de producciones por fecha:
    @action(methods=['get'], detail=False)
    def ReporteProduccionesPorFecha(self, request):
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')
        producciones = Producciones.objects.filter(FechaProduccion__range=[fecha_inicio, fecha_fin])
        serializer = ProduccionesSerializer(producciones, many=True)
        return Response(status=status.HTTP_200_OK, data={'reporte': serializer.data})










