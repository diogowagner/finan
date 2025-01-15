from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from fluxo.models import Lancamento, Item
from fluxo.forms import (
                    LancamentosObForm, 
                    AnexoForm, ItemForm,
                    TransferenciaForm,
                    )

@login_required
def transferir(request):

    if request.method == 'POST':
        valor = request.POST['valor']
        valor = float(valor.replace('.', '').replace(',', '.'))
        valor = Decimal(f'{valor:.2f}')

        valores = request.POST.copy()
        valores['valor'] = valor
        valores['valor_total'] = 0

        transferenciaForm = TransferenciaForm(valores)
        anexoForm = AnexoForm(request.POST, request.FILES)

        if transferenciaForm.is_valid():
            print(request.POST)
            data_lancamento = valores['data_transferencia']
            observacoes = valores['observacoes']
            conta_origem = int(valores['conta_origem'])
            conta_destino = int(valores['conta_destino'])
            descricao = valores['descricao']

            if conta_origem != conta_destino:
                lanc_origem = Lancamento.objects.create(
                                                        data_lancamento = data_lancamento,
                                                        observacoes = observacoes,
                                                        tipo = 'DESPESA',
                                                        valor_total = valor * -1,
                                                        situacao = 'PAGO',
                                                        conta_id = conta_origem
                                                        )
                lanc_origem.save()

                item_origem = Item.objects.create(
                                                    descricao = descricao,
                                                    valor = valor * -1,
                                                    categoria_id = 180,
                                                    lancamento_id = lanc_origem.id,
                                                )
                item_origem.save()

                if anexoForm.is_valid():
                    arquivos = anexoForm.save(commit=False)
                    arquivos.lancamento = lanc_origem
                    arquivos.save()

                lanc_destino = Lancamento.objects.create(
                                                        data_lancamento = data_lancamento,
                                                        observacoes = observacoes,
                                                        tipo = 'RECEITA',
                                                        valor_total = valor,
                                                        situacao = 'PAGO',
                                                        conta_id = conta_destino
                                                        )
                lanc_destino.save()

                item_destino = Item.objects.create(
                                                    descricao = descricao,
                                                    valor = valor,
                                                    categoria_id = 180,
                                                    lancamento_id = lanc_destino.id,
                                                )
                item_destino.save()

                transferenciaForm.save()

                if anexoForm.is_valid():
                    arquivos = anexoForm.save(commit=False)
                    arquivos.lancamento = lanc_destino
                    arquivos.save()

                return redirect('/lancamentos/todos/')

            else:
                messages.warning(request, 'A conta destino deve ser diferente da conta origem!')
                return redirect('/transferir/')

    else:
        transferenciaForm = TransferenciaForm()
        itemForm = ItemForm()
        anexoForm = AnexoForm()

    context = {
        'titulo': 'Adicionar transferência',
        'transferenciaForm': transferenciaForm,
        'anexoForm': anexoForm,
    }

    return render(request, 'transferir.html', context)