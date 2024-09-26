from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from Seguridad.Usuario.models import Usuario

@admin.register(Usuario)

class UsuarioAdmin(UserAdmin):
    pass

# Register your models here.
