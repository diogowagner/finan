from django.urls import path

from .views import(
                    inicio, 
                    adicionar_lancamento,
                    lancamentos, 
                    editar_lancamento,
                    filtros,
                    cadastro_categoria,
                    cadastro_conta,
                    cadastro_cliente_fornecedor,
                    login_view,
                    logout_view,
                    transferir,
                    relatorio_fluxo,
                    relatorio_lancamentos,
                    exportar_relatorio_excel,
                    )

app_name = 'fluxo'

urlpatterns = [    
    path('adicionar/<str:tipo>/', adicionar_lancamento, name='adicionar_lancamento'),
    path('editar/<str:tipo>/<int:ad>/<int:id>/', editar_lancamento, name='editar_lancamento'),
    path('transferir/', transferir, name='transferir'),
    path('cadastro/categoria/', cadastro_categoria, name='cadastro_categoria'),
    path('cadastro/conta/', cadastro_conta, name='cadastro_conta'),
    path('cadastro/<str:tipo>/', cadastro_cliente_fornecedor, name='cadastro_cliente_fornecedor'),
    path('filtros/', filtros, name='filtros'),
    path('relatorios/fluxo/', relatorio_fluxo, name='relatorio_fluxo'),
    path('relatorios/lancamentos/', relatorio_lancamentos, name='relatorio_lancamentos'),
    path('relatorio-lancamentos/exportar/', exportar_relatorio_excel, name='exportar_relatorio_excel'),
    path('lancamentos/<str:filtro>/', lancamentos, name='lancamentos'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', inicio, name='inicio'),
]