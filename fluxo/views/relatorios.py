from decimal import Decimal
from django.shortcuts import render
from fluxo.models import Item, Lancamento
from finan.models import Categoria
from datetime import datetime, date, timedelta
from fluxo.forms import (
                    ItemFormOp, 
                    )
from django.contrib.auth.decorators import login_required


@login_required
def relatorio_fluxo(request):
    itens = Item.objects.select_related('categoria', 'lancamento').all().filter(lancamento__situacao='PAGO')
    categorias = Categoria.objects.all().filter(ativo=True)
    
    relatorio = []

    categoria_totais = {}

    # Inicializa os totais das categorias
    for categoria in categorias:
        categoria_totais[categoria.id] = {
            'descricao': categoria.descricao,
            'valor_mes': [Decimal('0.00')] * 12,  # Inicializa uma lista com 12 zeros, um para cada mês
            'valor_total': Decimal('0.00')
        }

    # Soma os valores por categoria e mês
    for item in itens:
        categoria_id = item.categoria.id
        mes = item.lancamento.data_lancamento.month
        valor = item.valor
        categoria_totais[categoria_id]['valor_mes'][mes - 1] += valor
        categoria_totais[categoria_id]['valor_total'] += valor

    # # Agrega valores das subcategorias na categoria pai
    # for categoria in categorias:
    #     if not categoria.is_categoria_filha:
    #         for subcategoria in categoria.categoria_set.all():
    #             for i in range(12):
    #                 print(categoria_totais[categoria.id]['valor_mes'][i])
    #                 # categoria_totais[categoria.id]['valor_mes'][i] += categoria_totais[subcategoria.id]['valor_mes'][i]
    #             # categoria_totais[categoria.id]['valor_total'] += categoria_totais[subcategoria.id]['valor_total']


    for categoria in categorias:
        if categoria.categoria_pai_id != None:
            for i in range(12):
                # print(categoria_totais[categoria.categoria_pai_id]['valor_mes'][i] + categoria_totais[categoria.id]['valor_mes'][i])
                categoria_totais[categoria.categoria_pai_id]['valor_mes'][i] += categoria_totais[categoria.id]['valor_mes'][i]
            categoria_totais[categoria.categoria_pai_id]['valor_total'] += categoria_totais[categoria.id]['valor_total']


    # Prepara o relatório final
    for categoria in categorias:
        if categoria_totais[categoria.id]['valor_total'] != 0:  # Verifica se há algum valor diferente de zero
            relatorio.append({
                'id': categoria.id,
                'descricao': categoria_totais[categoria.id]['descricao'],
                'valor_mes': categoria_totais[categoria.id]['valor_mes'],
                'valor_total': categoria_totais[categoria.id]['valor_total'],
            })

    context = {
        'relatorio': relatorio,
        'titulo': 'Relatórios',
    }

    return render(request, 'relatorio_fluxo.html', context)

@login_required
def relatorio_lancamentos(request):
    itens = Item.objects.select_related('categoria', 'lancamento').all().filter(lancamento__situacao='PAGO')
    categorias = Categoria.objects.all().filter(ativo=True)

    print(request.GET)

    relatorio = []

    situacao_selecionada = request.GET.get('situacao')
    filtro_data = request.GET.get('filtro_data')

    # Recuperar ou definir datas da sessão
    data_inicio = request.session.get('data_inicio', None)
    data_fim = request.session.get('data_fim', None)

    # Se estiverem presentes no GET, atualizar os valores e a sessão
    if 'data_inicio' in request.GET and 'data_fim' in request.GET:
        data_inicio = request.GET.get('data_inicio')
        data_fim = request.GET.get('data_fim')
        request.session['data_inicio'] = data_inicio
        request.session['data_fim'] = data_fim


    # categoria_selecionada = request.session.get('categoria_selecionada', None)

    # Se estiver presente no GET, atualizar o valor e a sessão
    # if 'categoria' in request.GET:
    categoria_selecionada = request.GET.get('categoria')
        # request.session['categoria_selecionada'] = categoria_selecionada
    
    # print(data_inicio)
    hoje = date.today()
    
    if filtro_data == 'hoje':
        data_inicio = hoje
        data_fim = hoje
    elif filtro_data == 'semana':
        data_inicio = hoje - timedelta(days=7)
        data_fim = hoje
    elif filtro_data == 'mes':
        data_inicio = hoje - timedelta(days=30)
        data_fim = hoje
    elif filtro_data == 'ano':
        data_inicio = hoje - timedelta(days=365)
        data_fim = hoje

    # Converter strings para objetos de data, se necessário
    if isinstance(data_inicio, str):
        try:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
        except ValueError:
            data_inicio = None

    if isinstance(data_fim, str):
        try:
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        except ValueError:
            data_fim = None

    if not data_inicio or not data_fim:
        data_inicio = hoje - timedelta(days=30)
        data_fim = hoje

    # Filtrar os lançamentos com base nos filtros aplicados
    lancamentos_list = Item.objects.filter(
        lancamento__data_lancamento__range=(data_inicio, data_fim)
    ).order_by("lancamento__data_lancamento", "lancamento__pk")

    filtro = 'pago'
    lancamentos_list = lancamentos_list.filter(lancamento__situacao=filtro.upper())

    if categoria_selecionada:
        lancamentos_list = lancamentos_list.filter(categoria_id=categoria_selecionada)


    itemForm = ItemFormOp()
    print(data_inicio)
    print(data_fim)

    context = {
        'relatorio': relatorio,
        'titulo': 'Relatório Lancamentos',
        'itemForm': itemForm,
        'lancamentos_list': lancamentos_list,
        'data_inicio': data_inicio.isoformat() if data_inicio else '',
        'data_fim': data_fim.isoformat() if data_fim else '',
    }

    return render(request, 'relatorio_lancamentos.html', context)


