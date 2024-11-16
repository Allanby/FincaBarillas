from django.urls import path, include

urlpatterns = [

    path('Usuario/', include('APPS.Seguridad.Usuario.urls')),
]