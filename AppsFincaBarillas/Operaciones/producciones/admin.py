from django.contrib import admin
from AppsFincaBarillas.Operaciones.producciones.models import Producciones

@admin.register(Producciones)
class ProduccionesAdmin(admin.ModelAdmin):
    list_display = ['Id_produccion', 'codigo_produccion', 'producto', 'calidad_cosecha', 'fecha_produccion', 'cantidad_producida', 'lapso_produccion']
    search_fields = ['codigo_produccion']
