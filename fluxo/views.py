from django.shortcuts import render, redirect, get_object_or_404
from .models import Lancamento, Anexo, Item
from django.core.paginator import Paginator
from .forms import LancamentosForm, AnexoForm, ItemForm
from django.http import QueryDict
from django.forms import modelformset_factory
from django.db.models import Sum
from datetime import datetime, date, timedelta

from . import forms, models

def index(request):

    context = {}

    return render(
        request,
        'index.html',
        context
    )

def filtros(request):

    context = {}

    return render(
        request,
        'filtros.html',
        context
    )

def lancamentos(request):
    titulo = 'Lista lançamentos'
    
    # Capturar os parâmetros de data da URL
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    # Definir a data atual
    hoje = date.today()
    
    # Converter as strings de data para objetos datetime, se disponíveis
    if data_inicio:
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
    else:
        data_inicio = hoje - timedelta(days=7)

    if data_fim:
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
    else:
        data_fim = hoje 
        
    # Filtrar os lançamentos pelo intervalo de datas, se disponível
    if data_inicio and data_fim:
        lancamentos_list = Lancamento.objects.filter(
            data_lancamento__range=(data_inicio, data_fim)
        ).order_by("-data_lancamento", "-pk").prefetch_related('itens')
    elif data_inicio:
        lancamentos_list = Lancamento.objects.filter(
            data_lancamento__gte=data_inicio
        ).order_by("-data_lancamento", "-pk").prefetch_related('itens')
    elif data_fim:
        lancamentos_list = Lancamento.objects.filter(
            data_lancamento__lte=data_fim
        ).order_by("-data_lancamento", "-pk").prefetch_related('itens')
    else:
        lancamentos_list = Lancamento.objects.order_by("-data_lancamento", "-pk").prefetch_related('itens')
    
    # Consulta para calcular o saldo geral somando todos os valores dos itens
    saldo_geral = Item.objects.all().aggregate(Sum('valor'))['valor__sum']
    saldo_geral = f'{saldo_geral:.2f}' if saldo_geral is not None else '0.00'

    # Calcular saldo anterior à data de início, se fornecida
    saldo_anterior = 0
    if data_inicio:
        saldo_anterior = Lancamento.objects.filter(data_lancamento__lt=data_inicio).aggregate(Sum('itens__valor'))['itens__valor__sum']
        saldo_anterior = saldo_anterior if saldo_anterior is not None else 0

    # Lista para armazenar os lançamentos com seus respectivos saldos
    lancamentos_com_saldos = []
    saldo_acumulado = saldo_anterior

    # Calcular os saldos sequencialmente na ordem correta
    for lancamento in reversed(lancamentos_list):  # Inverte a ordem dos lançamentos
        saldo_lancamento = sum(item.valor for item in lancamento.itens.all())
        saldo_acumulado += saldo_lancamento
        lancamentos_com_saldos.append({
            'lancamento': lancamento,
            'saldo': saldo_acumulado,
        })

    paginator = Paginator(lancamentos_com_saldos, 10)
    page_number = request.GET.get('page')
    lancamentos_paginados = paginator.get_page(page_number)

    if lancamentos_paginados:
        primeiro_item = lancamentos_paginados[0]['lancamento'].data_lancamento
    else:
        primeiro_item = None
    
    # Construir os parâmetros de query string para a paginação
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()

    # Formatar as datas para o formato YYYY-MM-DD
    data_inicio_str = data_inicio.strftime('%Y-%m-%d')
    data_fim_str = data_fim.strftime('%Y-%m-%d')

    # Contexto para enviar ao template
    context = {
        'titulo': titulo,
        'is_lancamento': True,
        'lancamentos_com_saldos': lancamentos_paginados,
        'parameters': parameters,
        'saldo_geral': saldo_geral,
        'saldo_anterior': saldo_anterior,
        'data_inicio': data_inicio_str,
        'data_fim': data_fim_str,
    }

    # Renderizar o template com o contexto
    return render(request, 'lancamento.html', context)


from django.forms.models import inlineformset_factory

def adicionar_lancamento(request, tipo):
    if request.method == 'POST':
        valor = request.POST['valor']
        if tipo == 'despesa':
            valor = float(valor.replace('.', '').replace(',', '.')) * -1
        else:  # tipo == 'receita'
            valor = float(valor.replace('.', '').replace(',', '.'))
        valor = f'{valor:.2f}'

        valores = request.POST.copy()
        valores['valor'] = valor
        valores['tipo'] = tipo.upper()
        valores['valor_total'] = 0

        lancamentoForm = LancamentosForm(valores)
        itemForm = ItemForm(valores)
        anexoForm = AnexoForm(request.POST, request.FILES)

        if lancamentoForm.is_valid():
            lancamento = lancamentoForm.save()
            valores['lancamento'] = lancamento.id
            itemForm = ItemForm(valores)

            if itemForm.is_valid():
                item = itemForm.save(commit=False)
                item.lancamento = lancamento
                lancamento.valor_total = item.valor
                item.save()
                lancamento.save()

            arquivos = anexoForm.cleaned_data.get('anexos', [])
            for arquivo in arquivos:
                Anexo.objects.create(lancamento=lancamento, arquivo=arquivo, descricao=request.POST.get('descricao', ''))

            return redirect('fluxo:lancamentos')

    else:
        lancamentoForm = LancamentosForm()
        itemForm = ItemForm()
        anexoForm = AnexoForm()

    context = {
        'tipo': 'Despesa' if tipo == 'despesa' else 'Receita',
        'simbolo': '-' if tipo == 'despesa' else '+',
        'cor': 'text-danger' if tipo == 'despesa' else 'text-primary',
        'titulo': 'Adicionar lançamentos',
        'tipo1': 'Pago' if tipo == 'despesa' else 'Recebido',
        'tipo2': 'À pagar' if tipo == 'despesa' else 'À receber',
        'lancamentoForm': lancamentoForm,
        'itemForm': itemForm,
        'anexoForm': anexoForm,
    }

    return render(request, 'ad_lancamento.html', context)

def edicao_lancamento(request, tipo, id):
    lancamento = get_object_or_404(Lancamento, id=id, tipo=tipo.upper())

    if request.method == 'POST':
        valor = request.POST['valor']
        if tipo == 'despesa':
            valor = float(valor.replace('.', '').replace(',', '.')) * -1
        else:  # tipo == 'receita'
            valor = float(valor.replace('.', '').replace(',', '.'))
        valor = f'{valor:.2f}'

        valores = request.POST.copy()
        valores['valor'] = valor
        valores['tipo'] = tipo.upper()
        valores['valor_total'] = 0

        lancamentoForm = LancamentosForm(valores, instance=lancamento)
        item = lancamento.itens.first() if lancamento.itens.exists() else None
        itemForm = ItemForm(valores, instance=item)
        anexoForm = AnexoForm(request.POST, request.FILES, instance=lancamento.anexos.first() if lancamento.anexos.exists() else None)

        if lancamentoForm.is_valid() and itemForm.is_valid() and anexoForm.is_valid():
            lancamento = lancamentoForm.save()

            valores['lancamento'] = lancamento.id
            itemForm = ItemForm(valores, instance=item)
            if itemForm.is_valid():
                item = itemForm.save(commit=False)
                item.lancamento = lancamento
                lancamento.valor_total += item.valor
                item.save()
                lancamento.save()

                anexo = anexoForm.save(commit=False)
                anexo.lancamento = lancamento
                anexo.save()

            return redirect('fluxo:lancamentos')

    else:
        valor_form = f'{abs(lancamento.itens.first().valor):.2f}' if lancamento.itens.exists() else ''
        lancamentoForm = LancamentosForm(instance=lancamento)
        itemForm = ItemForm(instance=lancamento.itens.first() if lancamento.itens.exists() else None, initial={'valor': valor_form})
        anexoForm = AnexoForm(instance=lancamento.anexos.first() if lancamento.anexos.exists() else None)

    context = {
        'tipo': 'Despesa' if tipo == 'despesa' else 'Receita',
        'simbolo': '-' if tipo == 'despesa' else '+',
        'cor': 'text-danger' if tipo == 'despesa' else 'text-primary',
        'titulo': 'Editar lançamento',
        'tipo1': 'Pago' if tipo == 'despesa' else 'Recebido',
        'tipo2': 'À pagar' if tipo == 'despesa' else 'À receber',
        'lancamentoForm': lancamentoForm,
        'itemForm': itemForm,
        'anexoForm': anexoForm,
        'lancamento_id': id,
        'apagar': True,
    }

    return render(request, 'ad_lancamento.html', context)