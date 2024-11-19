from django.contrib import admin
from AppsFincaBarillas.Operaciones.detallePedido.models import DetallePedido

@admin.register(DetallePedido)
class DetallePedidoAdmin(admin.ModelAdmin):
    list_display = ['id', 'pedido', 'producto', 'cantidad']
    search_fields = ['id', 'pedido__id']  # Búsqueda por ID de detalle o ID de pedido
