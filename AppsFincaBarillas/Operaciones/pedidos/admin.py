from django.contrib import admin
from AppsFincaBarillas.Operaciones.pedidos.models import Pedidos

@admin.register(Pedidos)
class PedidosAdmin(admin.ModelAdmin):
    list_display = ['id_pedido', 'cliente', 'fecha_pedido', 'estado']  # Corrección de nombres
    search_fields = ['fecha_pedido']  # Buscar por fecha de pedido
