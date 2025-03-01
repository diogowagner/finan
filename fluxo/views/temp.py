from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from fluxo.models import Lancamento, Anexo, Item
from django.core.paginator import Paginator
from fluxo.forms import (
                    LancamentosOpForm, 
                    LancamentosObForm, 
                    AnexoForm, ItemForm, 
                    CategoriaForm, 
                    ContaForm,
                    FornecedorClienteForm,
                    CentroCustoForm,
                    )
from django.http import QueryDict
from django.forms import modelformset_factory
from django.db.models import Sum
from datetime import datetime, date, timedelta
from django.contrib.auth.decorators import login_required


from .. import forms, models


@login_required
def cadastro_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/lancamentos/todos/')
    else:
        form = CategoriaForm()
    
    context = {
        'form': form,
        'titulo': 'Criar Categoria'
    }
    return render(request, 'cad_categoria.html', context)

@login_required
def cadastro_conta(request):
    if request.method == 'POST':
        form = ContaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/lancamentos/todos/')
    else:
        form = ContaForm()
    
    context = {
        'form': form,
        'titulo': 'Criar Conta'
    }
    return render(request, 'cad_conta.html', context)

@login_required
def cadastro_cliente_fornecedor(request, tipo):
    if request.method == 'POST':
        valores = request.POST.copy()
        valores['tipo'] = tipo

        form = FornecedorClienteForm(valores)
        if form.is_valid():
            form.save()
            return redirect('/lancamentos/todos/')
    else:
        form = FornecedorClienteForm()
    
    context = {
        'form': form,
        'tipo': tipo,
        'titulo': 'Criar Fornecedor' if tipo == 'FORNECEDOR' else 'Criar Cliente',
    }
    return render(request, 'cad_cliente_fornecedor.html', context)

@login_required
def filtros(request):

    context = {}

    return render(
        request,
        'filtros.html',
        context
    )

@login_required
def cadastro_centro_custo(request):
    if request.method == 'POST':
        form = CentroCustoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/lancamentos/todos/')
    else:
        form = CentroCustoForm()
    
    context = {
        'form': form,
        'titulo': 'Criar Centro de Custo'
    }
    return render(request, 'cad_centro_custo.html', context)