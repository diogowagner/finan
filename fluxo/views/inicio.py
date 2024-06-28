from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from fluxo.models import Lancamento
from finan.models import Conta
from django.db.models import Sum

@login_required
def inicio(request):

    apagar = Lancamento.objects.all().filter(situacao='APAGAR')[:10]

    lista_saldos =[]
    for i in Conta.objects.all():
        saldo = Lancamento.objects.all().filter(
                            conta_id=i.id).aggregate(Sum('valor_total'))['valor_total__sum']
        if saldo is None:
            saldo = 0
        conta_saldo = {
                        'apelido':i.apelido_conta,
                        'saldo': saldo,
               }
        lista_saldos.append(conta_saldo)

    context = {
        'is_inicio': True,
        'apagar': apagar,
        'lista_saldos': lista_saldos,
    }

    return render(
        request,
        'inicio.html',
        context
    )