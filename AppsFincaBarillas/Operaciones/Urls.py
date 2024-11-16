from rest_framework.routers import DefaultRouter
from AppsFincaBarillas.Operaciones.detallePedido.API.DetallePedidoAPI import DetallePedidoViewSet
from AppsFincaBarillas.Operaciones.detalleVenta.API.DetalleVentaAPI import DetalleVentaViewSet
from AppsFincaBarillas.Operaciones.pedidos.API.PedidosAPI import PedidosViewSet
from AppsFincaBarillas.Operaciones.producciones.API.ProduccionesAPI import ProduccionesViewSet
from AppsFincaBarillas.Operaciones.ventas.API.VentasAPI import VentaViewSet






routerOperaciones = DefaultRouter()

routerOperaciones.register(prefix= 'detallePedido', basename='detallePedido', viewset= DetallePedidoViewSet)
routerOperaciones.register(prefix= 'detalleVenta', basename='detalleVenta', viewset=DetalleVentaViewSet)
routerOperaciones.register(prefix= 'pedidos', basename='pedidos', viewset=PedidosViewSet)
routerOperaciones.register(prefix= 'producciones', basename='producciones', viewset=ProduccionesViewSet)
routerOperaciones.register(prefix= 'ventas', basename='ventas', viewset=VentaViewSet) 





