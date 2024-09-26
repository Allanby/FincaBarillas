from django.contrib import admin
from AppsFincaBarillas.Operaciones.detallePedido.models import DetallePedido

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ['id_detalle_pedido', 'pedido', 'producto', 'cantidad']
    search_fields = ['id_detalle_pedido', 'pedido__id']  # Búsqueda por ID de detalle o ID de pedido
