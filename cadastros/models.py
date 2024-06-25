from django.db import models


class FornecedorCliente(models.Model):
    TIPO_CHOICES = (
        ('CLIENTE', 'Cliente'),
        ('FORNECEDOR', 'Fornecedor'),
    )
    cpf_cnpj = models.CharField(verbose_name='Cpf | Cnpj', max_length=20)
    nome_razao_social = models.CharField(verbose_name='Nome | Razão social',max_length=100)
    nome_fantasia = models.CharField(max_length=100, blank=True, null=True)
    ie = models.CharField(max_length=20, blank=True, null=True)
    im = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    cep = models.CharField(max_length=10, blank=True, null=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    numero = models.CharField(max_length=10, blank=True, null=True)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    estado = models.CharField(max_length=50, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    banco = models.CharField(max_length=100, blank=True, null=True)
    agencia = models.CharField(max_length=20, blank=True, null=True)
    conta = models.CharField(max_length=50, blank=True, null=True)
    observacao = models.TextField(blank=True, null=True)
    anexos = models.FileField(upload_to='anexos/', blank=True, null=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)

    def __str__(self):
        return self.nome_razao_social
