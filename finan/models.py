from django.db import models
from colorfield.fields import ColorField
from utils.rands import slugify_new, random_color

class Categoria(models.Model):
    class Meta:
        ordering = ['descricao']

    MISTA = 'MI'
    DESPESA = 'DE'
    RECEITA = 'RE'
    CLASSIFICACAO_ESCOLHAS = {
        MISTA: 'Mista',
        DESPESA: 'Despesa',
        RECEITA: 'Receita',
    }
    descricao = models.CharField(verbose_name='descricao', max_length=200, default='')
    cor = ColorField(auto_created=True, max_length=7)
    ativo = models.BooleanField(default=True)
    is_categoria_filha = models.BooleanField(verbose_name='Categoria filha', default=False)
    slug = models.SlugField(
        unique=True, default=None,
        blank=True, max_length=255,
    )
    categoria_pai = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='Categoria pai',
    )
    classificacao = models.CharField(
        max_length=3,
        choices=CLASSIFICACAO_ESCOLHAS,
        default=MISTA,
    )
    data_criada = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_new(self.descricao, 4)
        if self.cor == '#FFFFFF':
            self.cor = random_color()
        return super().save(*args, **kwargs)

    def __str__(self):
        return str(self.descricao)


class Empresa(models.Model):
    class Meta:
        verbose_name_plural = "Minha empresa"
        
    logotipo = models.ImageField(upload_to='logotipos/', blank=True, null=True)
    nome_fantasia = models.CharField('nome fantasia', max_length=100)
    razao_social = models.CharField('razao social', max_length=100)
    cnpj_cpf = models.CharField('CPF/CNPJ', max_length=14)
    insc_estadual = models.CharField('I.E.', max_length=18, blank=True, null=True)
    insc_municipal = models.CharField('I.M.', max_length=18, blank=True, null=True)
    endereco = models.CharField(max_length=200)
    numero = models.CharField(max_length=10)
    complemento = models.CharField(max_length=100, blank=True, null=True)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    cep = models.CharField(max_length=9)
    telefone = models.CharField(max_length=15)
    site_empresa = models.URLField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=254)
    setor_empresa = models.CharField(max_length=100)
    ramo_atuacao = models.CharField(max_length=100)
    produtos_servicos = models.TextField()
    numero_empregados = models.IntegerField()
    data_criacao = models.DateField()

    def __str__(self):
        return self.nome_fantasia

class Conta(models.Model):
    TIPO_CONTA_CHOICES = (
        ('Conta Corrente', 'Conta Corrente'),
        ('Poupança', 'Poupança'),
    )

    TIPO_CHAVE_PIX_CHOICES = (
        ('CPF/CNPJ', 'CPF/CNPJ'),
        ('E-mail', 'E-mail'),
        ('Telefone', 'Telefone'),
        ('Aleatória', 'Aleatória'),
    )

    tipo_conta = models.CharField(max_length=20, choices=TIPO_CONTA_CHOICES)
    banco = models.CharField(max_length=100)
    agencia = models.CharField(max_length=10)
    conta = models.CharField(max_length=15)
    gerente = models.CharField(max_length=100)
    telefone = models.CharField(max_length=15)
    apelido_conta = models.CharField(max_length=150)
    data_inicio = models.DateField()
    saldo_inicial = models.DecimalField(max_digits=15, decimal_places=2)
    saldo_conta = models.DecimalField(max_digits=15, decimal_places=2)  # Ajustado max_digits
    tipo_chave_pix = models.CharField(max_length=20, choices=TIPO_CHAVE_PIX_CHOICES)  # Corrigido para usar choices
    chave_pix = models.CharField(max_length=100)
    situacao_conta = models.CharField(max_length=100)
    agrupamento = models.CharField(max_length=100)
    permite_lancamentos = models.BooleanField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.apelido_conta


class CentroCusto(models.Model):
    TIPO_CENTRO_CHOICES = (
        ('Centro de custo/lucro pai', 'Centro de custo/lucro pai'),
        ('Centro de custo/lucro filho', 'Centro de custo/lucro filho'),
    )
    descricao = models.CharField(verbose_name='descricao', max_length=200, default='')
    tipo_centro_custo = models.CharField(max_length=100, choices=TIPO_CENTRO_CHOICES)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.descricao

class FormaPagamento(models.Model):
    descricao = models.CharField(verbose_name='descricao', max_length=200, default='')
    ativa = models.BooleanField(default=True)

    def __str__(self):
        return self.descricao

class Tag(models.Model):
    tag = models.CharField(verbose_name='tags', max_length=100)

    def __str__(self):
        return self.tag


