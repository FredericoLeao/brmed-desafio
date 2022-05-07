from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.db import IntegrityError

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brmeddesafio.settings')

app = Celery('brmeddesafio')

app.config_from_object('django.conf:settings', namespace='CELERY')

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute='0,2,4', hour=1),
        fetch_and_save_currency_quotation.s(),
        name='fetch currency quotation')


@app.task
def fetch_and_save_currency_quotation():
    import requests
    import json
    from currency_quotator.models import CurrencyRate
    quotation = requests.get('https://api.vatcomply.com/rates?base=USD')
    if quotation.status_code != 200:
        return False
    quotation_json = quotation.json()
    currency_rate = CurrencyRate()
    currency_rate.date = quotation_json['date']
    currency_rate.base = quotation_json['base']
    currency_rate.rates = json.dumps(quotation_json['rates'])
    try:
        currency_rate.save()
    except IntegrityError:
        # If for some reason we received a duplicated date, we can just ignore
        # it, as it can happen in two situations: a) This function was called
        # twice or more in the same day. b) Today is not a 'business day' and thus
        # the vatcomply API answers with the last 'business day's' quotation.
        pass
