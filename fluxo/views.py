from django.shortcuts import render, redirect, get_object_or_404
from .models import Lancamento, Anexo, Item
from django.core.paginator import Paginator
from .forms import (
                    LancamentosOpForm, 
                    LancamentosObForm, 
                    AnexoForm, ItemForm, 
                    CategoriaForm, 
                    ContaForm,
                    FornecedorClienteForm,
                    )
from django.http import QueryDict
from django.forms import modelformset_factory
from django.db.models import Sum
from datetime import datetime, date, timedelta

from . import forms, models

def index(request):
    if request.method == 'GET':
        return redirect('/lancamentos/')

    context = {
        'is_inicio': True,
    }

    return render(
        request,
        'index.html',
        context
    )

def cadastro_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/lancamentos/')
    else:
        form = CategoriaForm()
    
    context = {
        'form': form,
        'titulo': 'Criar Categoria'
    }
    return render(request, 'cad_categoria.html', context)

def cadastro_conta(request):
    if request.method == 'POST':
        form = ContaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/lancamentos/')
    else:
        form = ContaForm()
    
    context = {
        'form': form,
        'titulo': 'Criar Conta'
    }
    return render(request, 'cad_conta.html', context)

def cadastro_cliente_fornecedor(request, tipo):
    if request.method == 'POST':
        valores = request.POST.copy()
        valores['tipo'] = tipo

        form = FornecedorClienteForm(valores)
        if form.is_valid():
            form.save()
            return redirect('/lancamentos/')
    else:
        form = FornecedorClienteForm()
    
    context = {
        'form': form,
        'tipo': tipo,
        'titulo': 'Criar Fornecedor' if tipo == 'FORNECEDOR' else 'Criar Cliente',
    }
    return render(request, 'cad_cliente_fornecedor.html', context)

def filtros(request):

    context = {}

    return render(
        request,
        'filtros.html',
        context
    )

def lancamentos(request):
    titulo = 'Lançamentos'

    situacao_selecionada = request.GET.get('situacao')
    filtro = request.GET.get('filtro')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    conta_selecionada = request.GET.get('conta')

    hoje = date.today()
    
    if filtro == 'hoje':
        data_inicio = hoje
        data_fim = hoje
    elif filtro == 'semana':
        data_inicio = hoje - timedelta(days=7)
        data_fim = hoje
    elif filtro == 'mes':
        data_inicio = hoje - timedelta(days=30)
        data_fim = hoje
    elif filtro == 'ano':
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

    if conta_selecionada:
        lancamentos_list = lancamentos_list.filter(conta_id=conta_selecionada)

    if situacao_selecionada:
        lancamentos_list = lancamentos_list.filter(situacao=situacao_selecionada)

    # Calcular saldo anterior considerando todos os lançamentos antes da data_inicio
    saldo_anterior = 0

    if data_inicio:
        saldo_anterior = Item.objects.filter(
            lancamento__data_lancamento__lt=data_inicio
        ).filter(lancamento__situacao='PAGO').aggregate(Sum('valor'))['valor__sum']
        saldo_anterior = saldo_anterior if saldo_anterior is not None else 0

    saldo_geral = Item.objects.all().aggregate(Sum('valor'))['valor__sum']
    saldo_geral = f'{saldo_geral:.2f}' if saldo_geral is not None else '0.00'

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
    }

    return render(request, 'lancamento.html', context)


def adicionar_lancamento(request, tipo):

    if request.method == 'POST':
        valor = request.POST['valor']
        valor = float(valor.replace('.', '').replace(',', '.'))
        if tipo == 'DESPESA':
            valor *= -1
        valor = f'{valor:.2f}'

        valores = request.POST.copy()
        valores['valor'] = valor
        valores['tipo'] = tipo
        valores['valor_total'] = 0

        lancamentoForm = LancamentosObForm(valores)
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
            print(anexoForm.is_valid())
            if anexoForm.is_valid():
                arquivos = anexoForm.save(commit=False)
                arquivos.lancamento = lancamento
                arquivos.save()
            if 'salvar_anexo' in request.POST:
                return redirect(f'/editar/{tipo}/{lancamento.id}')
            else:
                return redirect('/lancamentos/')
            
    else:
        lancamentoForm = LancamentosObForm()
        itemForm = ItemForm()
        anexoForm = AnexoForm()

    context = {
        'tipo': tipo.capitalize(),
        'simbolo': '+' if tipo == 'RECEITA' else '-',
        'cor': 'text-primary' if tipo == 'RECEITA' else 'text-danger',
        'titulo': f'Adicionar {tipo.lower()}',
        'tipo1': 'Recebido' if tipo == 'RECEITA' else 'Pago',
        'tipo2': 'À receber' if tipo == 'RECEITA' else 'À pagar',
        'lancamentoForm': lancamentoForm,
        'itemForm': itemForm,
        'anexoForm': anexoForm,
    }

    return render(request, 'ad_lancamento.html', context)

def editar_lancamento(request, tipo, ad, id):
    try:
        lancamento = Lancamento.objects.get(id=id, tipo=tipo.upper())
    except Lancamento.DoesNotExist:
        return redirect('/lancamentos/')

    if request.method == 'POST':
        if 'delete' in request.POST:
            lancamento.delete()
            return redirect('/lancamentos/')

        elif 'salvar_anexo' in request.POST:
            anexoForm = AnexoForm(request.POST, request.FILES)
            if anexoForm.is_valid():
                    arquivos = anexoForm.save(commit=False)
                    arquivos.lancamento = lancamento
                    arquivos.save()
                    return redirect(f'/editar/{tipo}/{lancamento.id}')

        anexos = lancamento.anexos.all()
        anexo_nome = []
        anexo_nome = [{'nome': str(anexo.arquivo)[7:]} for anexo in anexos]


        valores = request.POST.copy()
        valores['valor_total'] = 0
        valores['tipo'] = tipo.upper()

        lancamentoForm = LancamentosObForm(valores, instance=lancamento)
        anexoForm = AnexoForm(request.POST, request.FILES)

        print(request.POST)

        if lancamentoForm.is_valid():
            lancamento = lancamentoForm.save()
            valores['lancamento'] = lancamento.id


            if 'valor' in request.POST:
                valor = request.POST['valor']
                valor = float(valor.replace('.', '').replace(',', '.'))
                if tipo == 'DESPESA':
                    valor *= -1
                valor = f'{valor:.2f}'
                valores[f'lancamento'] = str(lancamento.id)
                valores[f'valor'] = valor
                itemForm = ItemForm(valores)
                print(valores)
                if itemForm.is_valid():
                    item = itemForm.save(commit=False)
                    item.lancamento = lancamento
                    lancamento.valor_total = item.valor
                    item.save()
                    lancamento.save()

            itemForms = []

            valores = request.POST.copy()
            valores['valor_total'] = 0
            valores['tipo'] = tipo.upper()

            print(lancamento.itens.all())
            for i, item in enumerate(lancamento.itens.all()):

                if 'valor' in request.POST:
                    if not request.POST['valor']:
                        valor = request.POST[f'{i}-valor']
                        valor = float(valor.replace('.', '').replace(',', '.'))
                        if tipo == 'DESPESA':
                            valor *= -1
                        valor = f'{valor:.2f}'
                        valores[f'{i}-lancamento'] = str(lancamento.id)
                        valores[f'{i}-valor'] = valor

                else:
                    valor = request.POST[f'{i}-valor']
                    valor = float(valor.replace('.', '').replace(',', '.'))
                    if tipo == 'DESPESA':
                        valor *= -1
                    valor = f'{valor:.2f}'
                    valores[f'{i}-lancamento'] = str(lancamento.id)
                    valores[f'{i}-valor'] = valor

                itemForm = ItemForm(valores, prefix=str(i), instance=item)
                itemForms.append(itemForm)
                if itemForm.is_valid():
                    item = itemForm.save(commit=False)
                    item.lancamento = lancamento
                    lancamento.valor_total += item.valor
                    item.save()
                    lancamento.save()

            if not 'arquivo' in request.POST:
                if anexoForm.is_valid():
                    arquivos = anexoForm.save(commit=False)
                    arquivos.lancamento = lancamento
                    arquivos.save()

            if 'salvar_itens' in request.POST:
                adiciona_itens = True
                return redirect(f'/editar/{tipo}/1/{lancamento.id}')
            else:
                return redirect('/lancamentos/')

    else:
        if ad:
            adiciona_itens = True
        else:
            adiciona_itens = False
        itemForms = []
        for i, item in enumerate(lancamento.itens.all()):
            item.valor = f'{abs(item.valor):.2f}'
            itemForms.append(ItemForm(prefix=str(i), instance=item))
            
        lancamentoForm = LancamentosObForm(instance=lancamento)
        itemForm = ItemForm()

        anexoForm = AnexoForm()
        anexos = lancamento.anexos.all()
        anexo_nome = []
        anexo_nome = [{'nome': str(anexo.arquivo)[7:]} for anexo in anexos]

    context = {
        'tipo': tipo.capitalize(),
        'simbolo': '+' if tipo == 'RECEITA' else '-',
        'cor': 'text-primary' if tipo == 'RECEITA' else 'text-danger',
        'titulo': f'Editar {tipo.lower()}',
        'tipo1': 'Recebido' if tipo == 'RECEITA' else 'Pago',
        'tipo2': 'À receber' if tipo == 'RECEITA' else 'À pagar',
        'lancamentoForm': lancamentoForm,
        'itemForms': itemForms,
        'itemForm': itemForm,
        'anexoForm': anexoForm,
        'anexos': anexos,
        'anexo_nome': anexo_nome,
        'lancamento_id': id,
        'apagar': True,
        'editar_lancamento': True,
        'adiciona_itens': adiciona_itens,
    }

    return render(request, 'ad_lancamento.html', context)
