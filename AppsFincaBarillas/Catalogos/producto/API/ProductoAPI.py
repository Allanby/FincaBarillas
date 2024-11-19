from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from AppsFincaBarillas.Catalogos.producto.API.Permission import IsAdminOrReadOnly
#IsAuthenticated: solo usuarios logeados en el panel adminitrativo
#IsAdminUser: solo los usuarios administradores podran acceder
#IsAuthenticatedOrReadOnly: solo los usuarios autenticado podran hacer CDU el resto solo lectura
#Existen otros y crear nuestros propios permisos
#AllowAny: para indicar que es un endpoit libre sin aunteticacion

from AppsFincaBarillas.Catalogos.producto.API.Serializer import ProductoSerializer
from AppsFincaBarillas.Catalogos.producto.models import producto
from AppsFincaBarillas.Catalogos.producto.API.Permission import IsAdminOrReadOnly

class ProductoViewSet(ViewSet):
    permission_classes = [IsAuthenticated] #[IsAdminOrReadOnly]
    queryset = producto.objects.all()
    serializer = ProductoSerializer

    def list(self, request):
        data = request
        serializer = ProductoSerializer(producto.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def retrieve(self, request, pk: int):
        serializer = ProductoSerializer(producto.objects.get(pk=pk))
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request):
        # producto.objects.create(Codigo=request.Post['Codigo'],Nombre=request.Post['Nombre'])
        serializer = ProductoSerializer(data=request.Post)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def update(self, request, pk: int):
        Producto = producto.objects.get(pk=pk)
        serializer = ProductoSerializer (instance=Producto, data=request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data= serializer.data)


    def delete(self, request, pk: int):
        Producto = producto.objects.get(pk=pk)
        serializer = ProductoSerializer(Producto)
        Producto.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)


    #Cambiar estado del producto a "descontinuado:

    @action(methods=['post'], detail=False)
    def CambiarEstadoProducto(self, request):
        id_producto = request.data.get('IdProducto')
        Producto = producto.objects.filter(IdProducto=id_producto).first()
        if Producto:
            Producto.estado = 'Descontinuado'
            Producto.save()
            return Response(status=status.HTTP_200_OK, data={'mensaje': 'Producto descontinuado'})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'mensaje': 'Producto no encontrado'})

    #Filtrar productos por nombre que inicie con P o F
    @action(methods=['post'], detail=False)
    def FiltrarNombreProducto(self, request):
        letra_inicial = request.data.get("letra_inicial")

        if letra_inicial not in ["P", "F"]:
            data = {'mensaje': 'La letra inicial debe ser P o F.'}
        else:
            Producto = producto.objects.filter(Nombre__startswith=letra_inicial)
            serializer = ProductoSerializer(Producto, many=True)
            data = {'mensaje': 'Productos filtrados', 'resultado': serializer.data}

        return Response(status=status.HTTP_200_OK, data=data)



        #Reporte de Productos Disponibles

    @action(methods=['get'], detail=False)
    def ReporteProductosDisponibles(self, request):
        productos_disponibles = producto.objects.filter(estado='DISPONIBLE').count()

        data = {'productos_disponibles': productos_disponibles}
        return Response(status=status.HTTP_200_OK, data={'reporte': data})








