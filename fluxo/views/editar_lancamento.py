from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from fluxo.models import Lancamento
from fluxo.forms import (
                    LancamentosObForm, 
                    AnexoForm, ItemForm,
                    )
from django.forms import modelformset_factory

@login_required
def editar_lancamento(request, tipo, ad, id):
    try:
        lancamento = Lancamento.objects.get(id=id, tipo=tipo.upper())
    except Lancamento.DoesNotExist:
        return redirect('/lancamentos/')

    if request.method == 'POST':
        # print(request.POST)
        if 'delete' in request.POST:
            lancamento.delete()
            return redirect('/lancamentos/')

        elif 'remover_item' in request.POST:
            id_item = request.POST['remover_item']
            id_item = lancamento.itens.get(id=id_item)
            id_item.delete()
            valor_total = 0
            for item in lancamento.itens.all():
                valor_total += item.valor
            lancamento.valor_total = valor_total
            lancamento.save()
            print(valor_total)
            return redirect(f'/editar/{tipo}/0/{lancamento.id}')


        elif 'salvar_anexo' in request.POST:
            anexoForm = AnexoForm(request.POST, request.FILES)
            if anexoForm.is_valid():
                    arquivos = anexoForm.save(commit=False)
                    arquivos.lancamento = lancamento
                    arquivos.save()
                    return redirect(f'/editar/{tipo}/0/{lancamento.id}')

        anexos = lancamento.anexos.all()
        anexo_nome = []
        anexo_nome = [{'nome': str(anexo.arquivo)[7:]} for anexo in anexos]


        valores = request.POST.copy()
        valores['valor_total'] = 0
        valores['tipo'] = tipo.upper()

        lancamentoForm = LancamentosObForm(valores, instance=lancamento)
        anexoForm = AnexoForm(request.POST, request.FILES)


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
                    valor_total = 0
                    for i in lancamento.itens.all():
                        valor_total += i.valor
                    lancamento.valor_total = Decimal(valor_total) + Decimal(valor)
                    item.save()
                    lancamento.save()

            itemForms = []

            valores = request.POST.copy()
            valores['valor_total'] = 0
            valores['tipo'] = tipo.upper()

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
            itemForms.append({
                            'item':ItemForm(prefix=str(i), instance=item),
                            'item_id': item.id
                            })
        quantidade_itens = lancamento.itens.count()
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
        'quantidade_itens': quantidade_itens,
    }

    return render(request, 'ad_lancamento.html', context)