import requests
import json
import datetime
from currency_quotator.models import CurrencyRate

def rates_initial_data_populate():
    CurrencyRate.objects.all().delete()
    start_date = datetime.date.today() - datetime.timedelta(days=30)
    end_date = datetime.date.today()
    fetch_date = start_date
    while fetch_date <= end_date:
        fetch_date_str = fetch_date.strftime('%Y-%m-%d')
        url = f'https://api.vatcomply.com/rates?base=USD&date={fetch_date_str}'
        print(f'Fetching data from: {url}')
        quotation = requests.get(url)
        if quotation.status_code != 200:
            continue
        quotation_json = quotation.json()
        if quotation_json['date'] != fetch_date_str:
            print(f'({fetch_date_str}): No quotation. Probably not a business'
                   ' day.')
            fetch_date = fetch_date + datetime.timedelta(days=1)
            continue
        currency_rate = CurrencyRate()
        currency_rate.date = quotation_json['date']
        currency_rate.base = quotation_json['base']
        currency_rate.rates = json.dumps(quotation_json['rates'])
        currency_rate.save()

        fetch_date = fetch_date + datetime.timedelta(days=1)
