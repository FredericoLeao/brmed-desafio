# Desafio de programação para vaga de desenvolvedor python, do grupo BRMed

## Descrição

- Deve-se salvar as cotações de moedas com base em USD, diariamente, utilizando a api https://www.vatcomply.com/documentation.
- Gráfico das cotações deve ser feito utilizando o highcharts.
- Filtro por período (data inicial e final), com intervalo máximo de 5 dias.
- Seleção da moeda a ser visualizada/cotada, podendo ser: Euro, Iene, ou Real.

## Sobre o desenvolvimento

- Template padrão do Django.
- Datepicker com js puro.
- Consumo dos dados via API utilizando JavaScript.
- Fornecimento dos dados via API com Rest Framework.
- Tarefa agendada utilizando Celery, para guardar a cotação diária automaticamente.
- Função para popular o banco de dados com a cotação dos últimos 30 dias.
