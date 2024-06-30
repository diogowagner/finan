from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from fluxo.models import Lancamento, Item
from django.core.paginator import Paginator
from fluxo.forms import (
                    LancamentosOpForm, 
                    )
from django.forms import modelformset_factory
from django.db.models import Sum
from datetime import datetime, date, timedelta

from .. import forms, models


@login_required
def lancamentos(request, filtro):
    titulo = 'Lançamentos'

    situacao_selecionada = request.GET.get('situacao')
    filtro_data = request.GET.get('filtro_data')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    conta_selecionada = request.GET.get('conta')

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
    else:
        if data_inicio and data_fim:
            try:
                data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
                data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
            except ValueError:
                data_inicio = hoje - timedelta(days=7)
                data_fim = hoje
        else:
            data_inicio = hoje - timedelta(days=7)
            data_fim = hoje

    # Filtrar os lançamentos com base nos filtros aplicados
    lancamentos_list = Lancamento.objects.filter(
        data_lancamento__range=(data_inicio, data_fim)
    ).order_by("data_lancamento", "pk").prefetch_related('itens')

    if data_inicio:
        saldo_anterior = Item.objects.filter(
            lancamento__data_lancamento__lt=data_inicio
        ).filter(lancamento__situacao='PAGO').aggregate(Sum('valor'))['valor__sum']
        saldo_anterior = saldo_anterior if saldo_anterior is not None else 0

    saldo_geral = Item.objects.all().aggregate(Sum('valor'))['valor__sum']
    saldo_geral = f'{saldo_geral:.2f}' if saldo_geral is not None else '0.00'


    if filtro == 'apagar' or filtro == 'pago':
        lancamentos_list = lancamentos_list.filter(situacao=filtro.upper())
        apagar = True
    else:
        apagar = False

    if conta_selecionada:
        lancamentos_list = lancamentos_list.filter(conta_id=conta_selecionada)

    if situacao_selecionada:
        lancamentos_list = lancamentos_list.filter(situacao=situacao_selecionada)

    # Calcular saldo anterior considerando todos os lançamentos antes da data_inicio
    saldo_anterior = 0

    # Calcular saldo acumulado para cada lançamento
    lancamentos_com_saldos = []
    saldo_acumulado = saldo_anterior
    total_entradas = 0
    total_saidas = 0

    for lancamento in lancamentos_list:
        saldo_lancamento = lancamento.valor_total
        quantidade_itens = (lancamento.itens.count())
        if lancamento.situacao == 'PAGO':
            saldo_acumulado += saldo_lancamento
        lancamentos_com_saldos.append({
            'lancamento': lancamento,
            'saldo': saldo_acumulado,
            'quantidade_itens': quantidade_itens,
        })
    paginator = Paginator(lancamentos_com_saldos, 20)
    page_number = request.GET.get('page')
    lancamentos_paginados = paginator.get_page(page_number)

    if situacao_selecionada == 'APAGAR':
        saldo_pagina = 0
    elif lancamentos_paginados:
        saldo_paginado = lancamentos_paginados[0]['saldo']
        if lancamentos_paginados[0]['lancamento'].situacao == 'PAGO':
            valor_total_paginado = lancamentos_paginados[0]['lancamento'].valor_total
        else:
            valor_total_paginado = 0
        saldo_anterior = saldo_paginado - valor_total_paginado
        saldo_pagina = saldo_anterior
    else:
        saldo_pagina = saldo_acumulado

    for lancamento in lancamentos_paginados:
        if lancamento['lancamento'].tipo == 'RECEITA' and lancamento['lancamento'].situacao == 'PAGO':
            total_entradas += lancamento['lancamento'].valor_total
        elif lancamento['lancamento'].tipo == 'DESPESA' and lancamento['lancamento'].situacao == 'PAGO':
            total_saidas += lancamento['lancamento'].valor_total
        if lancamento['lancamento'].situacao == 'PAGO':
            saldo_pagina += lancamento['lancamento'].valor_total
        
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()

    lancamentoForm = LancamentosOpForm(initial={'conta': conta_selecionada, 'situacao': situacao_selecionada})

    context = {
        'titulo': titulo,
        'is_lancamento': True,
        'lancamentos_paginados': lancamentos_paginados,
        'parameters': parameters,
        'saldo_pagina': saldo_pagina,
        'saldo_anterior': saldo_anterior,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'data_inicio': data_inicio.isoformat() if data_inicio else '',
        'data_fim': data_fim.isoformat() if data_fim else '',
        'hoje': hoje.isoformat(),
        'lancamentoForm': lancamentoForm,
        'apagar':apagar,
    }

    return render(request, 'lancamento.html', context)