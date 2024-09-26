from django.contrib import admin
from AppsFincaBarillas.Operaciones.ventas.models import Venta

@admin.register(Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = ['id_venta', 'cliente', 'numero_venta', 'metodo_pago', 'fecha_venta', 'monto_total']
    search_fields = ['numero_venta']  # Corregido de 'N_Venta' a 'numero_venta' para que coincida con el modelo

