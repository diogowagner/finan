from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from fluxo.models import Lancamento
from finan.models import Conta
from django.db.models import Sum
from datetime import date, timedelta

@login_required
def inicio(request):

    # Obtém a data de início e fim do mês atual
    hoje = date.today()
    data_inicio = date(hoje.year, hoje.month, 1)

    # Calcula a data do primeiro dia do próximo mês
    if hoje.month == 12:  # Se for dezembro, o próximo mês é janeiro do próximo ano
        data_fim = date(hoje.year + 1, 1, 1) - timedelta(days=1)
    else:
        data_fim = date(hoje.year, hoje.month + 1, 1) - timedelta(days=1)
        
    apagar = Lancamento.objects.filter(
        data_lancamento__range=(data_inicio, data_fim)
    ).order_by("data_lancamento", "pk").prefetch_related('itens').filter(situacao='APAGAR')

    # apagar = Lancamento.objects.all().filter(situacao='APAGAR').order_by('data_lancamento')[:10]

    lista_saldos =[]
    for i in Conta.objects.all():
        saldo = Lancamento.objects.all().filter(
                            conta_id=i.id, situacao='PAGO').aggregate(Sum('valor_total'))['valor_total__sum']
        if saldo is None:
            saldo = 0
        conta_saldo = {
                        'apelido':i.apelido_conta,
                        'saldo': saldo,
               }
        lista_saldos.append(conta_saldo)

    saldo_total = 0

    for i in lista_saldos:
        saldo_total += i['saldo']

    context = {
        'is_inicio': True,
        'apagar': apagar,
        'lista_saldos': lista_saldos,
        'saldo_total': saldo_total,
    }

    return render(
        request,
        'inicio.html',
        context
    )