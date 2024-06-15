from django.db import models
from finan.models import Conta, Categoria
from cadastros.models import FornecedorCliente

class Lancamento(models.Model):
    DESPESA = 'DESPESA'
    RECEITA = 'RECEITA'
    DESPESA_RECEITA_CHOICES = [
        (DESPESA, 'Despesa'),
        (RECEITA, 'Receita'),
    ]

    PAGO = 'PAGO'
    APAGAR = 'APAGAR'
    PAGO_APAGAR_CHOICES = [
        (PAGO, 'Pago'),
        (APAGAR, 'À Pagar'),
    ]

    conta = models.ForeignKey(
        Conta,
        on_delete=models.CASCADE,
        blank=False, null=False,
        verbose_name="Conta"
    )
    data_lancamento = models.DateField(verbose_name="Data do Lançamento")
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
    competencia = models.DateField(blank=True, null=True, verbose_name="Competência")
    tipo_documento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tipo de Documento")
    numero_documento = models.CharField(max_length=100, blank=True, null=True, verbose_name="Número do Documento")
    tipo = models.CharField(max_length=20, choices=DESPESA_RECEITA_CHOICES, verbose_name="Tipo")
    valor_total = models.DecimalField(max_digits=10, decimal_places=2)
    situacao = models.CharField(max_length=20, choices=PAGO_APAGAR_CHOICES, default='PAGO', verbose_name="Situação")

    def __str__(self):
        return f'{self.data_lancamento} - {self.tipo}'



class Anexo(models.Model):
    lancamento = models.ForeignKey(
        Lancamento, 
        related_name='anexos', 
        on_delete=models.CASCADE,
        verbose_name="Lançamento"
    )
    arquivo = models.FileField(upload_to='anexos/', verbose_name="Arquivo", blank=True, null=True)

    def __str__(self):
        return f"Anexo para {self.lancamento.data_lancamento} - {self.lancamento.tipo}"


class Item(models.Model):
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        blank=False, null=False,
        verbose_name="Categoria"
    )
    centro_custo_lucro = models.CharField(max_length=100, blank=True, null=True)
    fornecedor_cliente = models.ForeignKey(
        FornecedorCliente,
        on_delete=models.CASCADE,
        blank=True, null=True,
        verbose_name="Fornecedor/Cliente"
    )
    forma_pagamento = models.CharField(max_length=100, blank=True, null=True)
    tag = models.CharField(max_length=100, blank=True, null=True)
    tipo_custo = models.CharField(max_length=100, blank=True, null=True)
    apropriacao_custo = models.CharField(max_length=100, blank=True, null=True)
    lancamento = models.ForeignKey(
        Lancamento,
        on_delete=models.CASCADE,
        related_name='itens',
        verbose_name="Lançamento"
    )

    def __str__(self):
        return f'{self.descricao} - {self.valor}'
