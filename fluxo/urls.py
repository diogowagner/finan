from django.urls import path

from .views import (index, 
                         adicionar_lancamento,
                         lancamentos, 
                         editar_lancamento,
                         filtros,
                        #  ad_item,
                        )

app_name = 'fluxo'

urlpatterns = [    
    path('adicionar/<str:tipo>/', adicionar_lancamento, name='adicionar_lancamento'),
    path('editar/<str:tipo>/<int:id>/', editar_lancamento, name='editar_lancamento'),
    # path('adiciona/item/', ad_item, name='ad_item'),
    path('filtros/', filtros, name='filtros'),
    path('lancamentos/', lancamentos, name='lancamentos'),
    path('', index, name='index'),
]