from django.shortcuts import render, redirect, get_object_or_404
from .models import Lancamento, Anexo, Item
from django.core.paginator import Paginator
from .forms import LancamentosForm, AnexoForm, ItemForm
from django.http import QueryDict
from django.forms import modelformset_factory

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
    item = Item.objects.order_by("-pk",)
    lancamentos_list = Lancamento.objects.order_by("-data_lancamento", "-pk").prefetch_related('itens')

    paginator = Paginator(lancamentos_list, 50)
    page = request.GET.get('page')
    lancamentos_paginados = paginator.get_page(page)

    get_copy = request.GET.copy()
    parameters = get_copy.pop('page',True) and get_copy.urlencode()

    context = {
        'titulo': titulo,
        'is_lancamento': True,
        'lancamentos': lancamentos_paginados,
        'item': item,
        'parameters': parameters,
    }

    return render(
        request,
        'lancamento.html',
        context
    )


from django.forms.models import inlineformset_factory

def ad_despesa(request):

    if request.method == 'POST':
        valor = request.POST['valor']
        valor = float(valor.replace('.', '').replace(',', '.')) * -1
        valor = f'{valor:.2f}'

        valores = request.POST.copy()
        valores['valor'] = valor
        valores['tipo'] = 'DESPESA'

        lancamentoForm = LancamentosForm(valores)
        itemForm = ItemForm(valores)
        if lancamentoForm.is_valid():
            lancamento = lancamentoForm.save()
            valores['lancamento'] = lancamento.id
            itemForm = ItemForm(valores)
            if itemForm.is_valid():
                item = itemForm.save(commit=False)
                item.lancamento = lancamento
                item.save()
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
        
        lancamentoForm = LancamentosForm(valores)
        itemForm = ItemForm(valores)
        print(lancamentoForm.is_valid())
        if lancamentoForm.is_valid():
            lancamento = lancamentoForm.save()

            valores['lancamento'] = lancamento.id
            itemForm = ItemForm(valores)
            print(itemForm.is_valid())
            print(itemForm.errors)
            if itemForm.is_valid():
                item = itemForm.save(commit=False)
                item.lancamento = lancamento
                item.save()

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
'''
def ed_despesa(request, despesa_id):

    lancamento = get_object_or_404(Lancamento, pk=despesa_id)
    AnexoFormSet = modelformset_factory(Anexo, form=AnexoForm, extra=1, can_delete=True)
    if request.method == 'POST':
        lancamentoForm = LancamentosForm(request.POST, instance=lancamento)
        formset = AnexoFormSet(request.POST, request.FILES, queryset=Anexo.objects.filter(lancamento=lancamento))
        if lancamentoForm.is_valid() and formset.is_valid():
            lancamento = lancamentoForm.save()
            for form in formset.cleaned_data:
                if form:
                    anexo = form['arquivo']
                    if anexo:
                        Anexo.objects.create(lancamento=lancamento, arquivo=anexo)
            return redirect('/lancamentos/')
    else:
        lancamentoForm = LancamentosForm(instance=lancamento)
        formset = AnexoFormSet(queryset=Anexo.objects.filter(lancamento=lancamento))

    context = {
        'tipo': 'Despesa',
        'simbolo': '-',
        'cor': 'text-danger',
        'titulo': 'Adicionar lançamentos',
        'tipo1': 'Pago',
        'tipo2': 'À pagar',
        'lancamentoForm': lancamentoForm,
        'formset': formset,
    }

    return render(
        request,
        'ad_lancamento.html',
        context
    )
'''
def ed_receita(request, receita_id):

    lancamento = get_object_or_404(Lancamento, pk=receita_id)
    AnexoFormSet = modelformset_factory(Anexo, form=AnexoForm, extra=1, can_delete=True)
    if request.method == 'POST':
        lancamentoForm = LancamentosForm(request.POST, instance=lancamento)
        formset = AnexoFormSet(request.POST, request.FILES, queryset=Anexo.objects.filter(lancamento=lancamento))
        if lancamentoForm.is_valid() and formset.is_valid():
            lancamento = lancamentoForm.save()
            for form in formset.cleaned_data:
                if form:
                    anexo = form['arquivo']
                    if anexo:
                        Anexo.objects.create(lancamento=lancamento, arquivo=anexo)
            return redirect('/lancamentos/')
    else:
        lancamentoForm = LancamentosForm(instance=lancamento)
        formset = AnexoFormSet(queryset=Anexo.objects.filter(lancamento=lancamento))

    context = {
        'tipo': 'Receita',
        'simbolo': '+',
        'cor': 'text-primary',
        'titulo': 'Adicionar lançamentos',
        'tipo1': 'Recebido',
        'tipo2': 'À receber',
        'lancamentoForm': lancamentoForm,
        'formset': formset,
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
