from decimal import Decimal
from django.shortcuts import render
from fluxo.models import Item
from finan.models import Categoria
from collections import defaultdict

# def relatorio_fluxo(request):
    
#     itens = Item.objects.select_related('categoria', 'lancamento').all()
#     categorias = Categoria.objects.all().filter(ativo=True)
        
#     relatorio = []

#     for categoria in categorias.values():
#         id = categoria['id']
#         descricao = categoria['descricao']
#         is_categoria_filha = categoria['is_categoria_filha']
#         valores_mes = []

#         for i in range(1,13):
#             valor_somado = 0
#             for item in itens:
#                 categoria_id = item.categoria.id
#                 mes = item.lancamento.data_lancamento.month
#                 valor = item.valor
#                 valor_mes = 0
#                 if id == categoria_id:
#                     if i == mes:
#                         valor_somado += valor
#             valor_mes = valor_somado
#             valores_mes.append(valor_mes)
#         if sum(valores_mes):
#             relatorio.append({
#                 'id': id,
#                 'descricao': descricao,
#                 'valor_mes': valores_mes,
#                 'valor_total': sum(valores_mes),
#             })

#     context = {
#         'relatorio': relatorio,
#         'titulo': 'Relatórios',
#     }

#     return render(request, 'relatorio_fluxo.html', context)


def relatorio_fluxo(request):
    itens = Item.objects.select_related('categoria', 'lancamento').all()
    categorias = Categoria.objects.all().filter(ativo=True)
    
    relatorio = []

    for categoria in categorias:
        id = categoria.id
        descricao = categoria.descricao
        is_categoria_filha = categoria.is_categoria_filha
        valores_mes = [0] * 12  # Inicializa uma lista com 12 zeros, um para cada mês

        for item in itens:
            if item.categoria.id == id:
                mes = item.lancamento.data_lancamento.month
                valores_mes[mes - 1] += item.valor  # Soma o valor no mês correto

        if any(valores_mes):  # Verifica se há algum valor diferente de zero
            relatorio.append({
                'id': id,
                'descricao': descricao,
                'valor_mes': valores_mes,
                'valor_total': sum(valores_mes),
            })

    context = {
        'relatorio': relatorio,
        'titulo': 'Relatórios',
    }

    return render(request, 'relatorio_fluxo.html', context)




# Exemplo de uso
# relatorio = relatorio_fluxo()
# for linha in relatorio:
#     print(f"Categoria: {linha['categoria']}")
#     for mes in range(1, 13):
#         print(f"  Mês {mes}: {linha[mes]}")






# def relatorio_fluxo(request):

#     categoria_pai = []
#     for i in Categoria.objects.all():
#         if not i.categoria_pai and not i.descricao == 'Transferência':
#             print(i)
#             categoria = {'categoria' : i.descricao}
#             categoria_pai.append(categoria)
#             quant_meses = 12
#             lista_mes = []
#             for mes in quant_meses:
#                 soma_mes = Item.objects.get(categoria_id = i.id).aggregate(Sum('valor'))['valor__sum']
#                 mes_soma = mes
#                 lista_mes.append({
#                     'mes_soma':mes_soma,
#                     'soma_mes':soma_mes
#                     })
#             categoria_pai.append(lista_mes)
        

#     context = {
#         'titulo': 'Relatórios'
#     }

#     return render(request, 'relatorio_fluxo.html', context)

'''
for i in Categoria.objects.all():
    ...:     print(i.descricao,'|', i.categoria_pai,'|', Item.objects.filter(categoria_id = i.id).aggregate(Sum('valor'))['valor__sum'])
    ...:     descricao = i.descricao
    ...:     categoria_pai_id = i.categoria_pai_id
    ...:     categoria_pai = i.categoria_pai
    ...:     valor_categoria = Item.objects.filter(categoria_id = i.id).aggregate(Sum('valor'))['valor__sum']
    ...:     categoria_list.append({
    ...:                           'descricao':descricao,
    ...:                           'categoria_pai_id':categoria_pai_id,
    ...:                           'categoria_pai':categoria_pai,
    ...:                           'valor_categoria':valor_categoria
    ...:                           })


for i in Categoria.objects.all():
     ...:     print(i.descricao,'|', i.categoria_pai,'|', Item.objects.filter(categoria_id = i.id).aggregate(Sum('valor'))['valor__sum'])
     ...:     descricao = i.descricao
     ...:     categoria_pai_id = i.categoria_pai_id
     ...:     if i.categoria_pai:
     ...:         categoria_pai = i.categoria_pai.descricao
     ...:     else:
     ...:         categoria_pai = None
     ...:     valor_categoria = Item.objects.filter(categoria_id = i.id).aggregate(Sum('valor'))['valor__sum']
     ...:     categoria_list.append({
     ...:                           'descricao':descricao,
     ...:                           'categoria_pai_id':categoria_pai_id,
     ...:                           'categoria_pai':categoria_pai,
     ...:                           'valor_categoria':valor_categoria
     ...:                           })
     
     
      for i in categoria_list:
     ...:     if i['categoria_pai_id'] is None and i['categoria_pai_id'] not in soma_categoria_pai:
     ...:         descricao = i['descricao']
     ...:         categoria_pai_id = i['categoria_pai_id']
     ...:         categoria_pai = i['categoria_pai']
     ...:         valor_categoria = i['valor_categoria']
     ...:         soma_categoria_pai.append({
     ...:                                     'descricao': descricao,
     ...:                                     'categoria_pai_id': categoria_pai_id,
     ...:                                     'categoria_pai': categoria_pai,
     ...:                                     'valor_categoria': valor_categoria,
     ...:                                  })
     ...:     elif i['categoria_pai_id'] in soma_categoria_pai:
     ...:         for l in soma_categoria_pai:
     ...:             if l['descricao'] == i['categoria_pai'].descricao:
     ...:                 print(l['valor_categoria'], i['valor_categoria'])
     
     
     
     
     
     '''