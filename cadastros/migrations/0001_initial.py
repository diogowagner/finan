# Generated by Django 5.0.4 on 2024-06-28 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FornecedorCliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cpf_cnpj', models.CharField(max_length=20, verbose_name='Cpf | Cnpj')),
                ('nome_razao_social', models.CharField(max_length=100, verbose_name='Nome | Razão social')),
                ('nome_fantasia', models.CharField(blank=True, max_length=100, null=True)),
                ('ie', models.CharField(blank=True, max_length=20, null=True)),
                ('im', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=100, null=True)),
                ('telefone', models.CharField(blank=True, max_length=20, null=True)),
                ('cep', models.CharField(blank=True, max_length=10, null=True)),
                ('endereco', models.CharField(blank=True, max_length=200, null=True)),
                ('numero', models.CharField(blank=True, max_length=10, null=True)),
                ('complemento', models.CharField(blank=True, max_length=100, null=True)),
                ('bairro', models.CharField(blank=True, max_length=100, null=True)),
                ('estado', models.CharField(blank=True, max_length=50, null=True)),
                ('cidade', models.CharField(blank=True, max_length=100, null=True)),
                ('banco', models.CharField(blank=True, max_length=100, null=True)),
                ('agencia', models.CharField(blank=True, max_length=20, null=True)),
                ('conta', models.CharField(blank=True, max_length=50, null=True)),
                ('observacao', models.TextField(blank=True, null=True)),
                ('anexos', models.FileField(blank=True, null=True, upload_to='anexos/')),
                ('tipo', models.CharField(choices=[('CLIENTE', 'Cliente'), ('FORNECEDOR', 'Fornecedor')], max_length=20)),
            ],
        ),
    ]
