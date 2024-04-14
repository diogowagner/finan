import csv
from django.db import transaction
from finan.models import Categoria

def importar_categorias(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)  # Pula o cabeçalho

        with transaction.atomic():
            categoria_pai = None
            identacao_anterior = 0

            for row in reader:
                descricao, cor, ativo, classificacao = row
                ativo = ativo.lower() == 'sim'
                identacao_atual = len(descricao) - len(descricao.lstrip())

                if identacao_atual > identacao_anterior:
                    # Esta é uma subcategoria da categoria anterior
                    categoria_pai = categoria
                elif identacao_atual < identacao_anterior:
                    # Esta é uma subcategoria da categoria avó
                    categoria_pai = categoria_pai.categoria_pai

                is_categoria_filha = categoria_pai is not None

                categoria = Categoria.objects.create(
                    descricao=descricao.strip(),
                    cor=cor,
                    ativo=ativo,
                    classificacao=classificacao,
                    categoria_pai=categoria_pai,
                    is_categoria_filha=is_categoria_filha,
                )

                identacao_anterior = identacao_atual
