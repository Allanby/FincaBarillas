from rest_framework.routers import DefaultRouter
from AppsFincaBarillas.Catalogos.cliente.API.ClienteAPI import ClienteViewSet
from AppsFincaBarillas.Catalogos.producto.API.ProductoAPI import ProductoViewSet
from AppsFincaBarillas.Catalogos.TipoProducto.API.TipoProductoAPI import TipoProductoViewSet





routerCatalogos = DefaultRouter()

routerCatalogos.register(prefix= 'Cliente', basename='Cliente', viewset=ClienteViewSet)
routerCatalogos.register(prefix= 'Producto', basename='Producto', viewset=ProductoViewSet)
routerCatalogos.register(prefix= 'TipoProducto', basename='TipoProducto', viewset=TipoProductoViewSet)



