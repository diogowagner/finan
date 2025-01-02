from django.http import HttpResponse
from openpyxl import Workbook
from datetime import datetime
from django.contrib.auth.decorators import login_required
from datetime import datetime, date, timedelta
from fluxo.models import Item

@login_required
def exportar_relatorio_excel(request):
    # Recupera os dados da sessão ou aplica os mesmos filtros usados na view
    data_inicio = request.session.get('data_inicio', None)
    data_fim = request.session.get('data_fim', None)
    categoria_selecionada = request.GET.get('categoria', None)

    # Converte strings para objetos de data
    if isinstance(data_inicio, str):
        data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
    if isinstance(data_fim, str):
        data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()

    if not data_inicio or not data_fim:
        data_inicio = datetime.now().date() - timedelta(days=30)
        data_fim = datetime.now().date()

    # Filtra os lançamentos
    lancamentos_list = Item.objects.filter(
        lancamento__data_lancamento__range=(data_inicio, data_fim),
        lancamento__situacao='PAGO'
    ).order_by("lancamento__data_lancamento", "lancamento__pk")

    if categoria_selecionada:
        lancamentos_list = lancamentos_list.filter(categoria_id=categoria_selecionada)

    # Cria um novo arquivo Excel
    workbook = Workbook()
    sheet = workbook.active
    sheet.title = "Relatório de Lançamentos"

    # Cabeçalhos da tabela
    sheet.append(["Data Lançamento", "Categoria", "Descrição", "Valor"])

    # Preenche os dados na planilha
    for item in lancamentos_list:
        sheet.append([
            item.lancamento.data_lancamento.strftime('%d-%m-%Y') if item.lancamento.data_lancamento else '',
            item.categoria.descricao if item.categoria else '',
            item.descricao,
            item.valor,
        ])

    # Configura a resposta HTTP
    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="relatorio_lancamentos.xlsx"'

    # Salva o arquivo Excel na resposta
    workbook.save(response)
    return response
