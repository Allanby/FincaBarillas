from django.contrib import admin
from AppsFincaBarillas.Catalogos.cliente.models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('id' ,'codigo', 'nombres', 'apellidos', 'telefono','direccion', 'estado')  # Campos mostrados en la tabla del admin
    search_fields = ('nombres', 'apellidos', 'telefono')  # Campos para el buscador
    list_filter = ('codigo', 'nombres', 'apellidos', 'telefono','direccion', 'estado')  # Filtrar por código
