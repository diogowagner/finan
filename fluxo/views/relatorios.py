from decimal import Decimal
from django.shortcuts import render
from fluxo.models import Item
from finan.models import Categoria
from collections import defaultdict


def relatorio_fluxo(request):
    itens = Item.objects.select_related('categoria', 'lancamento').all().filter(lancamento__situacao='PAGO')
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


