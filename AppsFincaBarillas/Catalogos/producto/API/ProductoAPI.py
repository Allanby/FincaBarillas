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
        productos = producto.objects.all()
        serializer = ProductoSerializer(productos, many=True)
        return Response(status=status.HTTP_200_OK, data={
            "success": True,
            "status": 200,
            "message": "Listado de productos",
            "record": serializer.data
        })

    def retrieve(self, request, pk: int):
        try:
            producto_obj = producto.objects.get(pk=pk)
            serializer = ProductoSerializer(producto_obj)
            return Response(status=status.HTTP_200_OK, data={
                "success": True,
                "status": 200,
                "message": "Producto encontrado",
                "record": serializer.data
            })
        except producto.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                "success": False,
                "status": 404,
                "message": "Producto no encontrado",
                "record": {}
            })

    def create(self, request):
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(status=status.HTTP_201_CREATED, data={
                "success": True,
                "status": 201,
                "message": "Producto creado exitosamente",
                "record": serializer.data
            })
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
            "success": False,
            "status": 400,
            "message": "Error al crear producto",
            "record": {}
        })

    def update(self, request, pk: int):
        try:
            producto_obj = producto.objects.get(pk=pk)
            serializer = ProductoSerializer(instance=producto_obj, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(status=status.HTTP_200_OK, data={
                    "success": True,
                    "status": 200,
                    "message": "Producto actualizado exitosamente",
                    "record": serializer.data
                })
        except producto.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                "success": False,
                "status": 404,
                "message": "Producto no encontrado",
                "record": {}
            })

    def delete(self, request, pk: int):
        try:
            producto_obj = producto.objects.get(pk=pk)
            producto_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT, data={
                "success": True,
                "status": 204,
                "message": "Producto eliminado exitosamente",
                "record": {}
            })
        except producto.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND, data={
                "success": False,
                "status": 404,
                "message": "Producto no encontrado",
                "record": {}
            })

    # Cambiar estado del producto a "descontinuado"
    @action(methods=['post'], detail=False)
    def CambiarEstadoProducto(self, request):
        id_producto = request.data.get('id_producto')
        producto_obj = producto.objects.filter(id_producto=id_producto).first()

        if producto_obj:
            producto_obj.estado = 'Descontinuado'
            producto_obj.save()
            return Response(status=status.HTTP_200_OK, data={
                "success": True,
                "status": 200,
                "message": "Producto descontinuado",
                "record": {
                    "id_producto": producto_obj.id_producto,
                    "estado": producto_obj.estado
                }
            })
        return Response(status=status.HTTP_400_BAD_REQUEST, data={
            "success": False,
            "status": 400,
            "message": "Producto no encontrado",
            "record": {}
        })

    # Filtrar productos por nombre que inicie con "P" o "F"
    @action(methods=['post'], detail=False)
    def FiltrarNombreProducto(self, request):
        letra_inicial = request.data.get("letra_inicial")

        if letra_inicial not in ["P", "F"]:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={
                "success": False,
                "status": 400,
                "message": "La letra inicial debe ser P o F.",
                "record": {}
            })

        productos = producto.objects.filter(nombre__startswith=letra_inicial)
        serializer = ProductoSerializer(productos, many=True)
        return Response(status=status.HTTP_200_OK, data={
            "success": True,
            "status": 200,
            "message": "Productos filtrados",
            "record": serializer.data
        })

    # Reporte de productos disponibles
    @action(methods=['get'], detail=False)
    def ReporteProductosDisponibles(self, request):
        productos_disponibles = producto.objects.filter(estado='DISPONIBLE').count()
        return Response(status=status.HTTP_200_OK, data={
            "success": True,
            "status": 200,
            "message": "Reporte de productos disponibles",
            "record": {
                "productos_disponibles": productos_disponibles
            }
        })