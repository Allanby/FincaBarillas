from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from AppsFincaBarillas.Catalogos.TipoProducto.API.Permission import IsAdminOrReadOnly
#IsAuthenticated: solo usuarios logeados en el panel adminitrativo
#IsAdminUser: solo los usuarios administradores podran acceder
#IsAuthenticatedOrReadOnly: solo los usuarios autenticado podran hacer CDU el resto solo lectura
#Existen otros y crear nuestros propios permisos
#AllowAny: para indicar que es un endpoit libre sin aunteticacion

from AppsFincaBarillas.Catalogos.TipoProducto.API.Serializer import TipoProductoSerializer
from AppsFincaBarillas.Catalogos.TipoProducto.models import TipoProducto
from AppsFincaBarillas.Catalogos.TipoProducto.API.Permission import IsAdminOrReadOnly

class TipoProductoViewSet(ViewSet):
    permission_classes = [IsAuthenticated] #[IsAdminOrReadOnly]
    queryset = TipoProducto.objects.all()
    serializer = TipoProductoSerializer

    def list(self, request):
        data = request
        serializer = TipoProductoSerializer(TipoProducto.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def retrieve(self, request, pk: int):
        serializer = TipoProductoSerializer(TipoProducto.objects.get(pk=pk))
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request):
        # TipoProducto.objects.create(Codigo=request.Post['Codigo'],Nombre=request.Post['Nombre'])
        serializer = TipoProductoSerializer(data=request.Post)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)


    def update(self, request, pk: int):
        tipoProducto = TipoProducto.objects.get(pk=pk)
        serializer = TipoProductoSerializer(instance=tipoProducto, data=request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data= serializer.data)


    def delete(self, request, pk: int):
        tipoProducto = TipoProducto.objects.get(pk=pk)
        serializer = TipoProductoSerializer(tipoProducto)
        tipoProducto.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

    #Filtrar por descripción que contenga "buena calidad"

    @action(methods=['post'], detail=False)
    def FiltrarPorCalidad(self, request):
        calidad = "buena calidad"
        tipos_producto = TipoProducto.objects.filter(Descripcion__icontains=calidad)
        serializer = TipoProductoSerializer(tipos_producto, many=True)
        data = {'mensaje': 'Tipos de producto con buena calidad', 'resultado': serializer.data}

        return Response(status=status.HTTP_200_OK, data=data)

        # Actualizar la calidad de un tipo de producto

    @action(methods=['post'], detail=False)
    def ActualizarCalidad(self, request):
        id_tipo = request.data.get('IdTipo')
        nueva_calidad = request.data.get('calidad')

        # Verifica que se haya proporcionado el IdTipo y la nueva calidad
        if not id_tipo or not nueva_calidad:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={'mensaje': 'IdTipo y calidad son requeridos'})

        # Busca el tipo de producto por su IdTipo
        tipo_producto = TipoProducto.objects.filter(IdTipo=id_tipo).first()
        if tipo_producto:
            tipo_producto.Descripcion = nueva_calidad  # el campo de calidad se almacena en "Descripcion"
            tipo_producto.save()
            return Response(status=status.HTTP_200_OK, data={'mensaje': 'Calidad actualizada'})

        return Response(status=status.HTTP_404_NOT_FOUND, data={'mensaje': 'Tipo de producto no encontrado'})

    #Listar Tipos de Producto por Popularidad:
    @action(methods=['get'], detail=False)
    def ListarPorPopularidad(self, request):
        tipos = TipoProducto.objects.annotate(num_ventas=Count('productos__detalle_venta')).order_by('-num_ventas')
        serializer = TipoProductoSerializer(tipos, many=True)
        return Response(status=status.HTTP_200_OK, data={'resultado': serializer.data})

    #Reporte de Tipos de Producto por Cantidad
    @action(methods=['get'], detail=False)
    def ReporteTiposProductoPorCantidad(self, request):
        tipos_producto_cantidad = TipoProducto.objects.values('Descripcion').annotate(
            cantidad_productos=Count('IdTipo')
        ).order_by('-cantidad_productos')

        data = [{'tipo_producto': t['Descripcion'], 'cantidad_productos': t['cantidad_productos']} for t in
                tipos_producto_cantidad]
        return Response(status=status.HTTP_200_OK, data={'reporte': data})









