from django.urls import path

from .views import(
                    index, 
                    adicionar_lancamento,
                    lancamentos, 
                    editar_lancamento,
                    filtros,
                    cadastro_categoria,
                    cadastro_conta,
                    cadastro_cliente_fornecedor,
                    )

app_name = 'fluxo'

urlpatterns = [    
    path('adicionar/<str:tipo>/', adicionar_lancamento, name='adicionar_lancamento'),
    path('editar/<str:tipo>/<int:ad>/<int:id>/', editar_lancamento, name='editar_lancamento'),
    path('cadastro/categoria/', cadastro_categoria, name='cadastro_categoria'),
    path('cadastro/conta/', cadastro_conta, name='cadastro_conta'),
    path('cadastro/<str:tipo>/', cadastro_cliente_fornecedor, name='cadastro_cliente_fornecedor'),
    path('filtros/', filtros, name='filtros'),
    path('lancamentos/', lancamentos, name='lancamentos'),
    path('', index, name='index'),
]