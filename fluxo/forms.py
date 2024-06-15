from django.forms import ModelForm, inlineformset_factory
from django import forms
from .models import Lancamento, Anexo, Item



class LancamentosForm(ModelForm):

    class Meta:
        model = Lancamento
        fields = ('__all__')
        widgets = {
            'conta': forms.Select(attrs={'class': "form-control"}),
            'data_lancamento': forms.DateInput(attrs={'class': "form-control", 'type': "date"}, format='%Y-%m-%d'),
            'observacoes': forms.Textarea(attrs={'rows': 5, 'class': "form-control"}),
            'competencia': forms.DateInput(attrs={'class': "form-control", 'type': "date"}),  # Adicionado para competência
            'tipo_documento': forms.TextInput(attrs={'class': "form-control"}),
            'numero_documento': forms.TextInput(attrs={'class': "form-control"}),
            'tipo': forms.HiddenInput(),
            'situacao': forms.RadioSelect(attrs={'class': "form-check"}),
        }

class ItemForm(ModelForm):

    class Meta:
        model = Item
        fields = ('__all__')
        widgets = {
            'descricao': forms.TextInput(attrs={'class':"form-control",'placeholder':"Descrição"}),
            'valor' : forms.TextInput(attrs={'class':"form-control valor",'placeholder':"0,00"}),
            'categoria': forms.Select(attrs={'class':"form-control"}),
            'centro_custo_lucro': forms.Select(attrs={'class':"form-control"}),
            'fornecedor_cliente': forms.Select(attrs={'class':"form-control"}),
            'forma_pagamento': forms.Select(attrs={'class':"form-control"}),
            'tag': forms.TextInput(attrs={'class':"form-control"}),
            'tipo_custo': forms.CheckboxInput(),
            'apropriacao_custo': forms.TextInput(attrs={'class': "form-control"}),
            'lancamento': forms.HiddenInput(),
        }

ItemFormSet = inlineformset_factory(Lancamento, Item, form=ItemForm, extra=1, can_delete=True)



class AnexoForm(forms.ModelForm):
    class Meta:
        model = Anexo
        fields = ['arquivo']
        widgets = {
            'arquivo': forms.FileInput(attrs={'class': "custom-file-input"})
        }