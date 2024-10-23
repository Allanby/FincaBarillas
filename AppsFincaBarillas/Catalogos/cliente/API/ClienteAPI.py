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

    #los del profe

    @action(methods=['get'], detail=False)
    def GetClienteByCodigo(self, request):
        codigo = request.GET.get("codigo")
        data = {'mensaje': f'Hola oliver{codigo}'}
        return Response(status=status.HTTP_200_OK, data=data)

    @action(methods=['post'], detail=False)
    def GetClienteByCodigoDescripcion(self, request):
        permission_classes=[AllowAny]
        # Capturar los datos del cuerpo del POST usando request.data
        codigo = request.data.get('Codigo')
        descripcion = request.data.get('Descripcion')

        # Crear una respuesta con los datos capturados
        data = {'mensaje': f'{codigo} - {descripcion}'}
        return Response(status=status.HTTP_200_OK, data=data)

    #LOS MIOS

    #Registrar clientes en modo inactivo
    @action(methods=['post'], detail=False)
    def RegistrarClientesInactivos(self, request):
        data_cliente = request.data
        data_cliente['Estado'] = 'Inactivo'
        serializer = ClienteSerializer(data=data_cliente)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK, data={'mensaje': 'Cliente registrado como inactivo'})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'mensaje': 'Datos inválidos'})



    #Actualizar direccion de cliente por codigo
    @action(methods=['post'], detail=False)
    def ActualizarDireccionPorCodigo(self, request):
        codigo = request.data.get('codigo')
        nueva_direccion = request.data.get('Direccion')
        Cliente = Cliente.objects.filter(codigo=codigo).first()
        if Cliente:
            Cliente.Direccion = nueva_direccion
            Cliente.save()
            return Response(status=status.HTTP_200_OK, data={'mensaje': 'Dirección actualizada'})
        return Response(status=status.HTTP_400_BAD_REQUEST, data={'mensaje': 'Cliente no encontrado'})


    #Filtrar clientes por dirección que inicie con M, G o R

    @action(methods=['post'], detail=False)
    def FiltrarDireccion(self, request):
        letra_inicial = request.data.get("letra_inicial")

        if letra_inicial not in ["M", "G", "R"]:
            data = {'mensaje': 'La letra inicial debe ser M, G o R.'}
        else:
            clientes = Cliente().objects.filter(Direccion__startswith=letra_inicial)
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














