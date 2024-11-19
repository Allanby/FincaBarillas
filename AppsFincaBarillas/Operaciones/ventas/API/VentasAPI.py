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

    @action(methods=['POST'], detail=False)
    def FiltrarVentasEfectivo(self, request):
        try:
            # Obtener el parámetro 'metodo_pago' de la solicitud, con un valor por defecto de 'Efectivo'
            metodo_pago = request.data.get('metodo_pago', 'Efectivo')  # 'Efectivo' por defecto
            monto_total = request.data.get('monto_total', 30000)  # 30,000 como valor por defecto

            # Filtrar ventas con los parámetros proporcionados
            ventas = Venta.objects.filter(metodo_pago=metodo_pago, monto_total__gt=monto_total)

            # Si no se encuentran ventas, devolver un mensaje adecuado
            if not ventas.exists():
                return Response(
                    {'mensaje': 'No se encontraron ventas con el criterio especificado.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            # Serializar los datos de las ventas
            serializer = VentaSerializer(ventas, many=True)
            data = {
                'mensaje': f'Ventas con método de pago {metodo_pago} y monto superior a {monto_total}',
                'resultado': serializer.data
            }

            # Devolver los resultados con código 200
            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'mensaje': 'Ocurrió un error inesperado', 'detalle': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        except Exception as e:
            # Si ocurre un error inesperado, lo manejamos aquí
            return Response(
                {'mensaje': 'Ocurrió un error inesperado', 'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    #Reporte de ventas por mes:
    @action(methods=['GET'], detail=False)
    def ReporteVentasPorMes(self, request):
        ventas_mes = Venta.objects.annotate(mes=TruncMonth('fecha_venta')).values('mes').annotate(
            total=sum('monto total')).order_by('mes')
        return Response(status=status.HTTP_200_OK, data={'reporte': ventas_mes})

    # Reporte de ventas por método de pago:
    @action(methods=['GET'], detail=False)
    def ReporteVentasPorMetodoPago(self, request):
        ventas_metodo = Venta.objects.values('metodo_pago').annotate(total_ventas=sum('monto_total'))
        return Response(status=status.HTTP_200_OK, data={'reporte': ventas_metodo})












