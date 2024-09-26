from django.contrib import admin

from AppsFincaBarillas.Catalogos import TipoProducto
from AppsFincaBarillas.Catalogos.TipoProducto.models import TipoProducto


@admin.register(TipoProducto)
class TipoProductoAdmin(admin.ModelAdmin):
    list_display = ['codigo','description']
    search_fields = ['description']
    list_filter = ['description']
# Register your models here.
