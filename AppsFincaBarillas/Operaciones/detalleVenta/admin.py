from django.contrib import admin
from AppsFincaBarillas.Operaciones.detalleVenta.models import DetalleVenta

@admin.register(DetalleVenta)
class DetalleVentaAdmin(admin.ModelAdmin):
    list_display = ['Id_DetalleVenta','venta', 'producto', 'descripcion', 'precio_producto', 'cantidad_producto']
    search_fields = ['descripcion']  # Búsqueda por descripción
