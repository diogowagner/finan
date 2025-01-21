from django.forms import ModelForm, inlineformset_factory
from django import forms
from .models import Lancamento, Anexo, Item, Categoria, FornecedorCliente, Conta, Transferencia, CentroCusto


class BaseLancamentosForm(ModelForm):
    class Meta:
        model = Lancamento
        fields = '__all__'
        widgets = {
            'conta': forms.Select(attrs={'class': 'form-control', 'data-placeholder':'Conta'}),
            'data_lancamento': forms.DateInput(attrs={'class': "form-control", 'type': "date"}, format='%Y-%m-%d'),
            'observacoes': forms.Textarea(attrs={'rows': 3, 'class': "form-control"}),
            'competencia': forms.DateInput(attrs={'class': "form-control", 'type': "date"}),  # Adicionado para competência
            'tipo_documento': forms.TextInput(attrs={'class': "form-control"}),
            'numero_documento': forms.TextInput(attrs={'class': "form-control"}),
            'tipo': forms.HiddenInput(),
            'situacao': forms.RadioSelect(attrs={'class': "form-check"}),
        }

class LancamentosOpForm(BaseLancamentosForm):
    class Meta(BaseLancamentosForm.Meta):
        pass  # Usa a Meta do formulário base

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['conta'].required = False  # Define o campo 'conta' como opcional
        self.fields['situacao'].required = False  # Define o campo 'situacao' como opcional

class LancamentosObForm(BaseLancamentosForm):
    class Meta(BaseLancamentosForm.Meta):
        pass  # Usa a Meta do formulário base

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['conta'].required = True  # Define o campo 'conta' como obrigatório



    class Meta:
        model = Lancamento
        fields = ('__all__')
        widgets = {
            'conta': forms.Select(attrs={'class': "form-control"}),
            'data_lancamento': forms.DateInput(attrs={'class': "form-control", 'type': "date"}, format='%Y-%m-%d'),
            'observacoes': forms.Textarea(attrs={'rows': 3, 'class': "form-control"}),
            'competencia': forms.DateInput(attrs={'class': "form-control", 'type': "date"}),  # Adicionado para competência
            'tipo_documento': forms.TextInput(attrs={'class': "form-control"}),
            'numero_documento': forms.TextInput(attrs={'class': "form-control"}),
            'tipo': forms.HiddenInput(),
            'situacao': forms.RadioSelect(attrs={'class': "form-check"}),
        }

class BaseItemForm(ModelForm):
    class Meta:
        model = Item
        fields = '__all__'
        widgets = {
            'id': forms.HiddenInput(),
            'descricao': forms.TextInput(attrs={'class': "form-control", 'placeholder': "Descrição"}),
            'valor': forms.TextInput(attrs={'class': "form-control valor", 'placeholder': "0,00"}),
            'categoria': forms.Select(attrs={'class': "form-control", 'placeholder': "Selecione uma categoria"}),
            'centro_custo_lucro': forms.Select(attrs={'class': "form-control", 'placeholder': "Selecione um centro de custo/lucro"}),
            'fornecedor_cliente': forms.Select(attrs={'class': "form-control", 'placeholder': "Selecione um fornecedor/cliente"}),
            'forma_pagamento': forms.Select(attrs={'class': "form-control", 'placeholder': "Selecione uma forma de pagamento"}),
            'tag': forms.TextInput(attrs={'class': "form-control"}),
            'tipo_custo': forms.CheckboxInput(),
            'apropriacao_custo': forms.TextInput(attrs={'class': "form-control"}),
            'lancamento': forms.HiddenInput(),
        }

class ItemForm(ModelForm):
    class Meta(BaseItemForm.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ordenar as categorias por nome
        self.fields['categoria'].queryset = Categoria.objects.filter(ativo=True).order_by('descricao')
        self.fields['categoria'].empty_label = "Selecione uma categoria"
        self.fields['centro_custo_lucro'].empty_label = "Centro de custo/lucro"
        self.fields['fornecedor_cliente'].empty_label = "Selecione um fornecedor/cliente"
        self.fields['forma_pagamento'].empty_label = "Forma de pagamento"


class ItemFormOp(BaseItemForm):
    class Meta(BaseItemForm.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].required = False  # Define o campo 'categoria' como opcional


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = [single_file_clean(data, initial)]
        return result

class AnexoForm(forms.ModelForm):
    class Meta:
        model = Anexo
        fields = ['arquivo']
        widgets = {
            'arquivo': forms.ClearableFileInput(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['arquivo'].required = False

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = (
            'descricao',
            'ativo',
            'is_categoria_filha',
            'categoria_pai',
            'classificacao',
        )
        widgets = {
            'descricao': forms.TextInput(attrs={'class':"form-control",'placeholder':"Descrição"}),            
            'ativo': forms.CheckboxInput(),
            'is_categoria_filha': forms.CheckboxInput(),
            'categoria_pai': forms.Select(attrs={'class':"form-control"}),
            'classificacao': forms.Select(attrs={'class':"form-control"}),
        }


class ContaForm(forms.ModelForm):
    class Meta:
        model = Conta
        fields = (
            'tipo_conta',
            'banco',
            'agencia',
            'conta',
            'gerente',
            'telefone',
            'apelido_conta',
            'data_inicio',
            'saldo_conta',
            'saldo_inicial',
            'tipo_chave_pix',
            'chave_pix',
            'situacao_conta',
            'agrupamento',
            'permite_lancamentos',
        )

        widgets = {
            'tipo_conta': forms.Select(attrs={'class':"form-control"}),
            'banco': forms.TextInput(attrs={'class':"form-control"}),
            'agencia': forms.TextInput(attrs={'class':"form-control"}),
            'conta': forms.TextInput(attrs={'class':"form-control"}),
            'gerente': forms.TextInput(attrs={'class':"form-control"}),
            'telefone': forms.TextInput(attrs={'class':"form-control"}),
            'apelido_conta': forms.TextInput(attrs={'class':"form-control"}),
            'data_inicio': forms.TextInput(attrs={'class':"form-control"}),
            'saldo_conta': forms.TextInput(attrs={'class':"form-control"}),
            'saldo_inicial': forms.TextInput(attrs={'class':"form-control"}),
            'tipo_chave_pix': forms.Select(attrs={'class':"form-control"}),
            'chave_pix': forms.TextInput(attrs={'class':"form-control"}),
            'situacao_conta': forms.TextInput(attrs={'class':"form-control"}),
            'agrupamento': forms.TextInput(attrs={'class':"form-control"}),
            'permite_lancamentos': forms.CheckboxInput(),
        }
        
class FornecedorClienteForm(forms.ModelForm):
    class Meta:
        model = FornecedorCliente
        fields = (
            'cpf_cnpj',
            'nome_razao_social',
            'nome_fantasia',
            'ie',
            'im',
            'email',
            'telefone',
            'cep',
            'endereco',
            'numero',
            'complemento',
            'bairro',
            'estado',
            'cidade',
            'banco',
            'agencia',
            'conta',
            'observacao',
            'tipo',
 
        )

        widgets = {
            'cpf_cnpj': forms.TextInput(attrs={'class':"form-control"}),
            'nome_razao_social': forms.TextInput(attrs={'class':"form-control"}),
            'nome_fantasia': forms.TextInput(attrs={'class':"form-control"}),
            'ie': forms.TextInput(attrs={'class':"form-control"}),
            'im': forms.TextInput(attrs={'class':"form-control"}),
            'email': forms.EmailInput(attrs={'class':"form-control"}),
            'telefone': forms.TextInput(attrs={'class':"form-control"}),
            'cep': forms.TextInput(attrs={'class':"form-control"}),
            'endereco': forms.TextInput(attrs={'class':"form-control"}),
            'numero': forms.TextInput(attrs={'class':"form-control"}),
            'complemento': forms.TextInput(attrs={'class':"form-control"}),
            'bairro': forms.TextInput(attrs={'class':"form-control"}),
            'estado': forms.TextInput(attrs={'class':"form-control"}),
            'cidade': forms.TextInput(attrs={'class':"form-control"}),
            'banco': forms.TextInput(attrs={'class':"form-control"}),
            'agencia': forms.TextInput(attrs={'class':"form-control"}),
            'conta': forms.TextInput(attrs={'class':"form-control"}),
            'observacao': forms.TextInput(attrs={'class':"form-control"}),
            'tipo': forms.HiddenInput(),
        }


class TransferenciaForm(forms.ModelForm):
    class Meta:
        model = Transferencia
        fields = '__all__'
        widgets = {
            'id': forms.HiddenInput(),
            'data_transferencia': forms.DateInput(attrs={'class': "form-control", 'type': "date"}, format='%Y-%m-%d'),
            'conta_origem': forms.Select(attrs={'class': 'form-control', 'data-placeholder':'Conta'}),
            'conta_destino': forms.Select(attrs={'class': 'form-control', 'data-placeholder':'Conta'}),
            'descricao': forms.TextInput(attrs={'class': "form-control", 'placeholder': "Descrição"}),
            'valor': forms.TextInput(attrs={'class': "form-control valor", 'placeholder': "0,00"}),
            'observacoes': forms.Textarea(attrs={'rows': 3, 'class': "form-control"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['descricao'].initial = "Transferência entre contas"


class CentroCustoForm(forms.ModelForm):
    class Meta:
        model = CentroCusto
        fields = (
            'descricao',
            'tipo_centro_custo',
        )

        widgets = {
            'descricao': forms.TextInput(attrs={'class':"form-control"}),
            'tipo_centro_custo': forms.Select(attrs={'class':"form-control"}),
        }