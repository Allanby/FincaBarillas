from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny


from AppsFincaBarillas.Operaciones.producciones.API.Serializer import ProduccionesSerializer
from AppsFincaBarillas.Operaciones.producciones.models import Producciones
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from collections import namedtuple

# Estructura de respuesta estandarizada
ResponseData = namedtuple('ResponseData', ['Success', 'Status', 'Message', 'Record'])

def to_response(data: ResponseData):
    return {
        "success": data.Success,
        "status": data.Status,
        "message": data.Message,
        "record": data.Record,
    }

class ProduccionesViewSet(ViewSet):
    permission_classes = [IsAuthenticated] #[IsAdminOrReadOnly]
    queryset = Producciones.objects.all()
    serializer = ProduccionesSerializer

    def list(self, request):
        try:
            producciones = Producciones.objects.all()
            serializer = ProduccionesSerializer(producciones, many=True)
            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message="Listado de producciones",
                Record=serializer.data
            )
            return Response(status=data.Status, data=to_response(data))
        except Exception as e:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                Message="Ocurrió un error inesperado",
                Record={"detalle": str(e)}
            )
            return Response(status=data.Status, data=to_response(data))

    def retrieve(self, request, pk: int):
        try:
            produccion = Producciones.objects.get(pk=pk)
            serializer = ProduccionesSerializer(produccion)
            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message="Producción encontrada",
                Record=serializer.data
            )
            return Response(status=data.Status, data=to_response(data))
        except Producciones.DoesNotExist:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message="Producción no encontrada",
                Record=None
            )
            return Response(status=data.Status, data=to_response(data))

    def create(self, request):
        try:
            serializer = ProduccionesSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = ResponseData(
                Success=True,
                Status=status.HTTP_201_CREATED,
                Message="Producción creada exitosamente",
                Record=serializer.data
            )
            return Response(status=data.Status, data=to_response(data))
        except Exception as e:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="Error al crear la producción",
                Record={"detalle": str(e)}
            )
            return Response(status=data.Status, data=to_response(data))

    def update(self, request, pk: int):
        try:
            produccion = Producciones.objects.get(pk=pk)
            serializer = ProduccionesSerializer(instance=produccion, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message="Producción actualizada exitosamente",
                Record=serializer.data
            )
            return Response(status=data.Status, data=to_response(data))
        except Producciones.DoesNotExist:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message="Producción no encontrada",
                Record=None
            )
            return Response(status=data.Status, data=to_response(data))

    def delete(self, request, pk: int):
        try:
            produccion = Producciones.objects.get(pk=pk)
            produccion.delete()
            data = ResponseData(
                Success=True,
                Status=status.HTTP_204_NO_CONTENT,
                Message="Producción eliminada exitosamente",
                Record=None
            )
            return Response(status=data.Status, data=to_response(data))
        except Producciones.DoesNotExist:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message="Producción no encontrada",
                Record=None
            )
            return Response(status=data.Status, data=to_response(data))

    @action(methods=['get'], detail=False)
    def FiltrarProduccionesPorFecha(self, request):
        fecha_inicio = request.query_params.get('FechaInicio')
        fecha_fin = request.query_params.get('FechaFin')

        if not fecha_inicio or not fecha_fin:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="FechaInicio y FechaFin son requeridos",
                Record=None
            )
            return Response(status=data.Status, data=to_response(data))

        producciones = Producciones.objects.filter(FechaProduccion__range=[fecha_inicio, fecha_fin])
        serializer = ProduccionesSerializer(producciones, many=True)
        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message="Producciones filtradas por fecha",
            Record=serializer.data
        )
        return Response(status=data.Status, data=to_response(data))

    @action(methods=['get'], detail=False)
    def ProduccionMasReciente(self, request):
        try:
            produccion = Producciones.objects.latest('FechaProduccion')
            serializer = ProduccionesSerializer(produccion)
            data = ResponseData(
                Success=True,
                Status=status.HTTP_200_OK,
                Message="Producción más reciente encontrada",
                Record=serializer.data
            )
            return Response(status=data.Status, data=to_response(data))
        except Producciones.DoesNotExist:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_404_NOT_FOUND,
                Message="No hay producciones registradas",
                Record=None
            )
            return Response(status=data.Status, data=to_response(data))

    @action(methods=['get'], detail=False)
    def ReporteProduccionesPorFecha(self, request):
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')

        if not fecha_inicio or not fecha_fin:
            data = ResponseData(
                Success=False,
                Status=status.HTTP_400_BAD_REQUEST,
                Message="fecha_inicio y fecha_fin son requeridos",
                Record=None
            )
            return Response(status=data.Status, data=to_response(data))

        producciones = Producciones.objects.filter(FechaProduccion__range=[fecha_inicio, fecha_fin])
        serializer = ProduccionesSerializer(producciones, many=True)
        data = ResponseData(
            Success=True,
            Status=status.HTTP_200_OK,
            Message="Reporte de producciones generado",
            Record=serializer.data
        )
        return Response(status=data.Status, data=to_response(data))








