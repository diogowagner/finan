from django.shortcuts import render, redirect, get_object_or_404
from .models import Lancamento, Anexo, Item
from django.core.paginator import Paginator
from .forms import LancamentosForm, AnexoForm, ItemForm
from django.http import QueryDict
from django.forms import modelformset_factory
from django.db.models import Sum

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
    
    # Consulta para pegar todos os itens
    itens = Item.objects.order_by("-pk")
    
    # Consulta para pegar todos os lançamentos ordenados pela data e ID
    lancamentos_list = Lancamento.objects.order_by("-data_lancamento", "-pk").prefetch_related('itens')
    
    # Consulta para calcular o saldo geral somando todos os valores dos itens
    saldo_geral = Item.objects.all().aggregate(Sum('valor'))['valor__sum']
    saldo_geral = f'{saldo_geral:.2f}' if saldo_geral is not None else '0.00'

    # Lista para armazenar os lançamentos com seus respectivos saldos
    lancamentos_com_saldos = []
    saldo_acumulado = 0

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
    
    # Construir os parâmetros de query string para a paginação
    get_copy = request.GET.copy()
    parameters = get_copy.pop('page', True) and get_copy.urlencode()
    print(lancamentos_com_saldos)
    print(lancamentos_paginados)

    # Contexto para enviar ao template
    context = {
        'titulo': titulo,
        'is_lancamento': True,
        'lancamentos_com_saldos': lancamentos_paginados,
        'itens': itens,  # Renomeei 'item' para 'itens' para ser mais descritivo
        'parameters': parameters,
        'saldo_geral': saldo_geral,
    }

    # Renderizar o template com o contexto
    return render(request, 'lancamento.html', context)


from django.forms.models import inlineformset_factory

def ad_despesa(request):

    if request.method == 'POST':
        valor = request.POST['valor']
        valor = float(valor.replace('.', '').replace(',', '.')) * -1
        valor = f'{valor:.2f}'

        valores = request.POST.copy()
        valores['valor'] = valor
        valores['tipo'] = 'DESPESA'
        valores['valor_total'] = 0

        lancamentoForm = LancamentosForm(valores)
        itemForm = ItemForm(valores)
        if lancamentoForm.is_valid():
            lancamento = lancamentoForm.save()
            valores['lancamento'] = lancamento.id
            itemForm = ItemForm(valores)
            if itemForm.is_valid():
                item = itemForm.save(commit=False)
                item.lancamento = lancamento
                lancamento.valor_total += item.valor
                item.save()
                lancamento.save()
            return redirect('/lancamentos/')
    else:
        lancamentoForm = LancamentosForm()
        itemForm = ItemForm()

    context = {
        'tipo': 'Despesa',
        'simbolo': '-',
        'cor': 'text-danger',
        'titulo': 'Adicionar lançamentos',
        'tipo1': 'Pago',
        'tipo2': 'À pagar',
        'lancamentoForm': lancamentoForm,
        'itemForm': itemForm,
        # 'formset': formset,
    }

    return render(request, 'ad_lancamento.html', context)


def ad_receita(request):

    if request.method == 'POST':
        valor = request.POST['valor']
        valor = float(valor.replace('.', '').replace(',', '.'))
        valor = f'{valor:.2f}'
        
        valores = request.POST.copy()
        valores['valor'] = valor
        valores['tipo'] = 'RECEITA'
        valores['valor_total'] = 0
        
        lancamentoForm = LancamentosForm(valores)
        itemForm = ItemForm(valores)
        print(lancamentoForm.is_valid())
        print(lancamentoForm.errors)
        if lancamentoForm.is_valid():
            lancamento = lancamentoForm.save()

            valores['lancamento'] = lancamento.id
            itemForm = ItemForm(valores)
            print(itemForm.is_valid())
            print(itemForm.errors)
            if itemForm.is_valid():
                item = itemForm.save(commit=False)
                item.lancamento = lancamento
                lancamento.valor_total += item.valor
                item.save()
                lancamento.save()

            return redirect('/lancamentos/')
    else:
        lancamentoForm = LancamentosForm()
        itemForm = ItemForm()

    context = {
        'tipo': 'Receita',
        'simbolo': '+',
        'cor': 'text-primary',
        'titulo': 'Adicionar lançamentos',
        'tipo1': 'Recebido',
        'tipo2': 'À receber',
        'lancamentoForm': lancamentoForm,
        'itemForm': itemForm,
    }

    return render(
        request,
        'ad_lancamento.html',
        context
    )

def ed_despesa(request, despesa_id):
    print(request)
    try:
        lancamento = Lancamento.objects.get(id=despesa_id, tipo='DESPESA')
    except Lancamento.DoesNotExist:
        return redirect('/lancamentos/')

    if request.method == 'POST':
        valor = request.POST['valor']
        valor = float(valor.replace('.', '').replace(',', '.')) * -1
        valor = f'{valor:.2f}'

        valores = request.POST.copy()
        valores['valor'] = valor
        valores['tipo'] = 'DESPESA'

        lancamentoForm = LancamentosForm(valores, instance=lancamento)
        itemForm = ItemForm(valores)

        if lancamentoForm.is_valid():
            lancamento = lancamentoForm.save()
            valores['lancamento'] = lancamento.id
            itemForm = ItemForm(valores, instance=lancamento.itens.first())

            if itemForm.is_valid():
                item = itemForm.save(commit=False)
                item.lancamento = lancamento
                item.save()

            return redirect('/lancamentos/')
    else:
        lancamentoForm = LancamentosForm(instance=lancamento)
        itemForm = ItemForm(instance=lancamento.itens.first())
        print(lancamentoForm)

    context = {
        'tipo': 'Despesa',
        'simbolo': '-',
        'cor': 'text-danger',
        'titulo': 'Editar lançamento',
        'tipo1': 'Pago',
        'tipo2': 'À pagar',
        'lancamentoForm': lancamentoForm,
        'itemForm': itemForm,
        'lancamento_id': despesa_id,
    }

    return render(request, 'ad_lancamento.html', context)

def ed_receita(request, receita_id):
    print(request)
    try:
        lancamento = Lancamento.objects.get(id=receita_id, tipo='RECEITA')
    except Lancamento.DoesNotExist:
        return redirect('/lancamentos/')

    if request.method == 'POST':
        valor = request.POST['valor']
        valor = float(valor.replace('.', '').replace(',', '.'))
        valor = f'{valor:.2f}'

        valores = request.POST.copy()
        valores['valor'] = valor
        valores['tipo'] = 'DESPESA'

        lancamentoForm = LancamentosForm(valores, instance=lancamento)
        itemForm = ItemForm(valores)

        if lancamentoForm.is_valid():
            lancamento = lancamentoForm.save()
            valores['lancamento'] = lancamento.id
            itemForm = ItemForm(valores, instance=lancamento.itens.first())

            if itemForm.is_valid():
                item = itemForm.save(commit=False)
                item.lancamento = lancamento
                item.save()

            return redirect('/lancamentos/')
    else:
        lancamentoForm = LancamentosForm(instance=lancamento)
        itemForm = ItemForm(instance=lancamento.itens.first())
        print(lancamentoForm)

    context = {
        'tipo': 'Receita',
        'simbolo': '+',
        'cor': 'text-danger',
        'titulo': 'Editar lançamento',
        'tipo1': 'Recebido',
        'tipo2': 'À receber',
        'lancamentoForm': lancamentoForm,
        'itemForm': itemForm,
        'lancamento_id': receita_id,
    }

    return render(request, 'ad_lancamento.html', context)
