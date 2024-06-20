from django.urls import path

from .views import (index, 
                         adicionar_lancamento,
                         lancamentos, 
                         edicao_lancamento,
                         filtros,
                        #  ad_item,
                        )

app_name = 'fluxo'

urlpatterns = [
    path('', index, name='index'),
    path('adicionar/<str:tipo>/', adicionar_lancamento, name='adicionar_lancamento'),
    path('editar/<str:tipo>/<int:id>/', edicao_lancamento, name='edicao_lancamento'),
    # path('adiciona/item/', ad_item, name='ad_item'),
    path('filtros/', filtros, name='filtros'),
    path('lancamentos/', lancamentos, name='lancamentos'),
]