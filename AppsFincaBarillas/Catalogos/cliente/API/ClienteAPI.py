from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny


from AppsFincaBarillas.Catalogos.cliente.API.Serializer import ClienteSerializer
from AppsFincaBarillas.Catalogos.cliente.models import Cliente
from AppsFincaBarillas.Catalogos.cliente.API.Permission import IsAdminOrReadOnly



class ClienteViewSet(ViewSet):
    permission_classes = [IsAuthenticated] #[IsAdminOrReadOnly]
    queryset = Cliente.objects.all()
    serializer = ClienteSerializer

    def list(self, request):
        serializer = ClienteSerializer(Cliente.objects.all(), many=True)
        data = {
            "Success": True,
            "Status": status.HTTP_200_OK,
            "Message": "Lista de clientes obtenida correctamente",
            "Records": serializer.data
        }
        return Response(status=status.HTTP_200_OK, data=data)

    def retrieve(self, request, pk: int):
        cliente = Cliente.objects.get(pk=pk)
        serializer = ClienteSerializer(cliente)
        data = {
            "Success": True,
            "Status": status.HTTP_200_OK,
            "Message": "Cliente obtenido correctamente",
            "Record": serializer.data
        }
        return Response(status=status.HTTP_200_OK, data=data)

    def create(self, request):
        serializer = ClienteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "Success": True,
            "Status": status.HTTP_201_CREATED,
            "Message": "Cliente creado correctamente",
            "Record": serializer.data
        }
        return Response(status=status.HTTP_201_CREATED, data=data)

    def update(self, request, pk: int):
        cliente = Cliente.objects.get(pk=pk)
        serializer = ClienteSerializer(instance=cliente, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        data = {
            "Success": True,
            "Status": status.HTTP_200_OK,
            "Message": "Cliente actualizado correctamente",
            "Record": serializer.data
        }
        return Response(status=status.HTTP_200_OK, data=data)

    def delete(self, request, pk: int):
        cliente = Cliente.objects.get(pk=pk)
        cliente.delete()
        data = {
            "Success": True,
            "Status": status.HTTP_204_NO_CONTENT,
            "Message": "Cliente eliminado correctamente"
        }
        return Response(status=status.HTTP_204_NO_CONTENT, data=data)

    @action(methods=['post'], detail=False)
    def ActualizarNombrePorCodigo(self, request):
        codigo = request.data.get('codigo')
        nuevo_nombre = request.data.get('Nombre')
        cliente = Cliente.objects.filter(codigo=codigo).first()
        if cliente:
            cliente.Nombre = nuevo_nombre
            cliente.save()
            data = {
                "Success": True,
                "Status": status.HTTP_200_OK,
                "Message": "Nombre del cliente actualizado correctamente"
            }
        else:
            data = {
                "Success": False,
                "Status": status.HTTP_400_BAD_REQUEST,
                "Message": "Cliente no encontrado"
            }
        return Response(status=data["Status"], data=data)

    @action(methods=['post'], detail=False)
    def FiltrarApellido(self, request):
        letra_inicial = request.data.get("letra_inicial")
        if letra_inicial not in ["M", "G", "R"]:
            data = {
                "Success": False,
                "Status": status.HTTP_400_BAD_REQUEST,
                "Message": "La letra inicial debe ser M, G o R"
            }
        else:
            clientes = Cliente.objects.filter(Apellido__startswith=letra_inicial)
            serializer = ClienteSerializer(clientes, many=True)
            data = {
                "Success": True,
                "Status": status.HTTP_200_OK,
                "Message": "Clientes filtrados correctamente",
                "Records": serializer.data
            }
        return Response(status=data["Status"], data=data)

    @action(methods=['post'], detail=False)
    def ContarPorApellido(self, request):
        apellido = request.data.get("apellido")
        if not apellido:
            data = {
                "Success": False,
                "Status": status.HTTP_400_BAD_REQUEST,
                "Message": "Debe proporcionar un apellido"
            }
        else:
            total = Cliente.objects.filter(Apellido=apellido).count()
            data = {
                "Success": True,
                "Status": status.HTTP_200_OK,
                "Message": f"Total de clientes con el apellido {apellido}: {total}",
                "Record": {"total": total}
            }
        return Response(status=data["Status"], data=data)

    @action(methods=['get'], detail=False)
    def BuscarPorTelefono(self, request):
        telefono = request.query_params.get('telefono', '')
        cliente = Cliente.objects.filter(Telefono__iexact=telefono).first()
        if cliente:
            serializer = ClienteSerializer(cliente)
            data = {
                "Success": True,
                "Status": status.HTTP_200_OK,
                "Message": "Cliente encontrado",
                "Record": serializer.data
            }
        else:
            data = {
                "Success": False,
                "Status": status.HTTP_404_NOT_FOUND,
                "Message": "Cliente no encontrado"
            }
        return Response(status=data["Status"], data=data)

    @action(methods=['get'], detail=False)
    def ReporteClientesPorEstado(self, request):
        # Filtramos los clientes por estado: 1 (activo) y 0 (inactivo)
        clientes_por_estado = Cliente.objects.filter(estado__in=[1, 0]).values('estado', 'codigo', 'nombres',
                                                                               'apellidos').order_by('estado')

        # Transformamos los resultados en un formato adecuado
        data = {
            "Success": True,
            "Status": status.HTTP_200_OK,
            "Message": "Reporte de clientes por estado generado correctamente",
            "Records": [
                {"Estado": "Activo" if c['estado'] == 1 else "Inactivo",
                 "Codigo": c['codigo'],
                 "Nombres": c['nombres'],
                 "Apellidos": c['apellidos']}
                for c in clientes_por_estado
            ]
        }

        return Response(status=data["Status"], data=data)










