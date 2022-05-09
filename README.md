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
- Tarefa agendada utilizando Celery com Redis, para guardar a cotação diária automaticamente.
- Função para preencher o banco de dados com a cotação dos últimos 30 dias.

## Instalação

- Necessário ter Redis instalado
- Clonar este repositório
- Criar um virtualenv  
    _python -m venv .venv_  
    _source .venv/bin/activate_
- Instalar os "requirements"  
    _python -m pip install -r requirements.txt_
- Configurar acesso ao Redis no arquivo brmeddesafio/settings.py.
  - Nas variáveis que começam com CELLERY_ configurar a senha e ip do servidor Redis.
- Executar migrations  
    _./manage.py migrate_
- Executar o servidor web do Django  
    _./manage runserver_
- Executar o celery worker  
    _celery -A brmeddesafio worker -l info_
- Executar o celery beat  
    _celery -A brmeddesafio beat -l info_
- Executar função para preencher o banco de dados  
    _./manage shell_  
    _from currency_quotator.utils import rates_initial_data_populate_  
    _rates_initial_data_populate()_
