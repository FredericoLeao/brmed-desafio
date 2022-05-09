from django.test import TestCase
from rest_framework.test import APIClient
from model_bakery import baker
import datetime

class CurrencyRateAPITestCase(TestCase):
    def setUp(self) -> None:
        # populate with some fake data
        end_date = datetime.date.today()
        start_date = end_date - datetime.timedelta(days=20)
        i_date = start_date
        while i_date <= end_date:
            baker.make(
                'currency_quotator.CurrencyRate',
                date=i_date,
                base='USD',
                rates='{"EUR":0.946073793755913, "USD":1.0, "JPY":130.4635761589404}' 
            )
            i_date = i_date + datetime.timedelta(days=1)

        return super().setUp()

    def test_api(self):
        client = APIClient()
        # Get status OK, defaults to the last 5 days  
        res = client.get('/api/rates/')
        self.assertEqual(res.status_code, 200)
        res = res.json()
        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 5)

        # Bad request, period length not permitted
        res = client.get('/api/rates/?start_date=20/04/2022&end_date=30/04/2022')
        self.assertEqual(res.status_code, 400)
        res_json = res.json()
        self.assertTrue('msg' in res_json)
        self.assertTrue('ultrapassar o intervalo de 5 dias' in res_json['msg'])

        # OK, 2 days period selected
        res = client.get('/api/rates/?start_date=02/05/2022&end_date=06/05/2022')
        self.assertEqual(res.status_code, 200)
        res = res.json()
        self.assertIsInstance(res, list)
        self.assertEqual(len(res), 5)
