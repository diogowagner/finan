from django.urls import path

from .views import(
                    usuario,
                    cria_usuario,
                    )

app_name = 'cadastro'

urlpatterns = [
    path('usuario', usuario, name='usuario'),
    path('usuario/criar', cria_usuario, name='cria_usuario'),
]