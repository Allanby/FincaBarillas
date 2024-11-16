from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly, AllowAny
from AppsFincaBarillas.Catalogos.cliente.API.Permission import IsAdminOrReadOnly
#IsAuthenticated: solo usuarios logeados en el panel adminitrativo
#IsAdminUser: solo los usuarios administradores podran acceder
#IsAuthenticatedOrReadOnly: solo los usuarios autenticado podran hacer CDU el resto solo lectura
#Existen otros y crear nuestros propios permisos
#AllowAny: para indicar que es un endpoit libre sin aunteticacion

from AppsFincaBarillas.Catalogos.cliente.API.Serializer import ClienteSerializer
from AppsFincaBarillas.Catalogos.cliente.models import Cliente
from AppsFincaBarillas.Catalogos.cliente.API.Permission import IsAdminOrReadOnly



class ClienteViewSet(ViewSet):
    permission_classes = [IsAuthenticated] #[IsAdminOrReadOnly]
    queryset = Cliente.objects.all()
    serializer = ClienteSerializer

    def list(self, request):
        data = request
        serializer = ClienteSerializer(Cliente.objects.all(), many=True)
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def retrieve(self, request, pk: int):
        serializer = ClienteSerializer(Cliente().objects.get(pk=pk))
        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def create(self, request):
        # Categoria.objects.create(Codigo=request.Post['Codigo'],Nombre=request.Post['Nombre'])
        serializer = ClienteSerializer(data=request.Post)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data=serializer.data)\

    def update(self, request, pk: int):
        cliente = Cliente.objects.get(pk=pk)
        serializer = ClienteSerializer(instance=cliente, data=request.data)
        serializer.is_valid(raise_exception= True)
        serializer.save()
        return Response(status=status.HTTP_200_OK, data= serializer.data)


    def delete(self, request, pk: int):
        cliente = Cliente.objects.get(pk=pk)
        serializer = ClienteSerializer(cliente)
        cliente.delete()
        return Response(status= status.HTTP_204_NO_CONTENT)

    #LOS MIOS allan

    # Actualizar nombre de cliente por código
    @action(methods=['post'], detail=False)
    def ActualizarNombrePorCodigo(self, request):
        codigo = request.data.get('codigo')
        nuevo_nombre = request.data.get('Nombre')
        cliente = Cliente.objects.filter(codigo=codigo).first()
        if cliente:
            cliente.Nombre = nuevo_nombre
            cliente.save()
            return Response(status=status.HTTP_200_OK, data={'mensaje': 'Nombre actualizado'})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'mensaje': 'Cliente no encontrado'})

    # Filtrar clientes por apellido que inicie con M, G o R
    @action(methods=['post'], detail=False)
    def FiltrarApellido(self, request):
        letra_inicial = request.data.get("letra_inicial")

        if letra_inicial not in ["M", "G", "R"]:
            data = {'mensaje': 'La letra inicial debe ser M, G o R.'}
        else:
            clientes = Cliente.objects.filter(Apellido__startswith=letra_inicial)
            serializer = ClienteSerializer(clientes, many=True)
            data = {'mensaje': 'Clientes filtrados', 'resultado': serializer.data}

        return Response(status=status.HTTP_200_OK, data=data)

    #Contar clientes con un apellido específico

    @action(methods=['post'], detail=False)
    def ContarPorApellido(self, request):
        apellido = request.data.get("apellido")

        if not apellido:
            data = {'mensaje': 'Debe proporcionar un apellido.'}
        else:
            total = Cliente.objects.filter(Apellidos=apellido).count()
            data = {'mensaje': f'Total de clientes con el apellido {apellido}: {total}'}

        return Response(status=status.HTTP_200_OK, data=data)

    #Buscar Cliente por Teléfono
    @action(methods=['get'], detail=False)
    def BuscarPorTelefono(self, request):
        telefono = request.query_params.get('telefono', '')
        cliente = Cliente.objects.filter(Telefono__iexact=telefono).first()
        if cliente:
            serializer = ClienteSerializer(cliente)
            data = {'mensaje': 'Cliente encontrado', 'resultado': serializer.data}
        else:
            data = {'mensaje': 'Cliente no encontrado'}
        return Response(status=status.HTTP_200_OK, data=data)

    #Reporte de Clientes por Estado
    @action(methods=['get'], detail=False)
    def ReporteClientesPorEstado(self, request):
        clientes_por_estado = Cliente.objects.values('Estado').annotate(
            total_clientes=Count('IdCliente')
        ).order_by('Estado')

        data = [{'estado': c['Estado'], 'total_clientes': c['total_clientes']} for c in clientes_por_estado]
        return Response(status=status.HTTP_200_OK, data={'reporte': data})











