from django.db import models
from finan.models import Conta, Categoria, FormaPagamento, CentroCusto
from cadastros.models import FornecedorCliente
from django.utils import timezone
import os

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
    arquivo = models.FileField(upload_to='anexos/')

    def save(self, *args, **kwargs):
        if self.arquivo and not self.pk:
            filename, ext = os.path.splitext(self.arquivo.name)
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            new_filename = f"{self.lancamento.id}_{timestamp}{ext}"
            self.arquivo.name = new_filename
        super(Anexo, self).save(*args, **kwargs)


class Item(models.Model):
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    categoria = models.ForeignKey(
        Categoria,
        on_delete=models.CASCADE,
        blank=False, null=False,
        verbose_name="Categoria",
    )
    centro_custo_lucro = models.ForeignKey(
        CentroCusto,
        on_delete=models.CASCADE,
        blank=True, null=True,
        verbose_name="Centro custo/lucro"
    )
    fornecedor_cliente = models.ForeignKey(
        FornecedorCliente,
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='fornecedor_cliente',
        verbose_name="Fornecedor/Cliente"
    )
    forma_pagamento = models.ForeignKey(
        FormaPagamento,
        on_delete=models.CASCADE,
        blank=True, null=True,
        related_name='forma_pagamento',
        verbose_name="Lançamento",
        )
    tag = models.CharField(max_length=100, blank=True, null=True)
    tipo_custo = models.CharField(max_length=100, blank=True, null=True)
    apropriacao_custo = models.CharField(max_length=100, blank=True, null=True)
    lancamento = models.ForeignKey(
        Lancamento,
        on_delete=models.CASCADE,
        related_name='itens',
        verbose_name="Lançamento",
    )

    def __str__(self):
        return f'{self.descricao} - {self.valor}'

class Transferencia(models.Model):
    data_transferencia = models.DateField(verbose_name="Data da Transferência")
    conta_origem = models.ForeignKey(
        Conta,
        on_delete=models.CASCADE,
        related_name='conta_origem',
        verbose_name="Conta origem",
    )
    conta_destino = models.ForeignKey(
        Conta,
        on_delete=models.CASCADE,
        related_name='conta_destino',
        verbose_name="Conta destino",
    )
    descricao = models.CharField(max_length=200)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    observacoes = models.TextField(blank=True, null=True, verbose_name="Observações")
