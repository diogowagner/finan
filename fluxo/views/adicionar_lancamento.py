from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta
from fluxo.forms import (
                    LancamentosObForm, 
                    AnexoForm, ItemForm, 
                    )

@login_required
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
        valor_parcelado = None
        if request.POST['parcelas']:
            parcelas = int(request.POST['parcelas'])
            if parcelas > 1:
                valor_parcelado = Decimal(valor) / parcelas

        if valor_parcelado and not 'salvar_itens' in request.POST:
            data_lancamento = datetime.strptime(valores['data_lancamento'], '%Y-%m-%d').date()
            for i in range(parcelas):
                lancamentoForm = LancamentosObForm(valores)
                itemForm = ItemForm(valores)
                anexoForm = AnexoForm(request.POST, request.FILES)

                if lancamentoForm.is_valid():
                    lancamento = lancamentoForm.save(commit=False)
                    if i > 0:
                        data_lancamento += timedelta(days=30)
                        lancamento.data_lancamento = data_lancamento
                    lancamento.save()
                    valores['lancamento'] = lancamento.id
                    itemForm = ItemForm(valores)
                    
                    if itemForm.is_valid():
                        item = itemForm.save(commit=False)
                        item.lancamento = lancamento
                        item.valor = valor_parcelado
                        item.descricao = f'{item.descricao} {i + 1} de {parcelas}'
                        lancamento.valor_total = item.valor
                        item.save()
                        lancamento.save()
                        
                    if anexoForm.is_valid():
                        arquivos = anexoForm.save(commit=False)
                        arquivos.lancamento = lancamento
                        arquivos.save()

        else:
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

                if anexoForm.is_valid():
                    arquivos = anexoForm.save(commit=False)
                    arquivos.lancamento = lancamento
                    arquivos.save()

        if 'salvar_anexo' in request.POST:
            return redirect(f'/editar/{tipo}/0/{lancamento.id}')
        elif 'salvar_itens' in request.POST:
                adiciona_itens = True
                return redirect(f'/editar/{tipo}/1/{lancamento.id}')
        else:
            return redirect('/lancamentos/todos/')
            
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
        'adiciona_lancamento': True,
    }

    return render(request, 'ad_lancamento.html', context)