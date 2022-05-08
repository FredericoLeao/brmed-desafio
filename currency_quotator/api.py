import datetime
import json
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.response import Response
from currency_quotator.models import CurrencyRate


class CurrencyRateAPIView(APIView):
    def get(self, request, **kwargs):
        start_date = request.GET.get('start_date', None)
        end_date = request.GET.get('end_date', None)
        if end_date:
            try:
                end_date = datetime.datetime.strptime(end_date, '%d/%m/%Y')
            except ValueError:
                return Response(status=HTTP_400_BAD_REQUEST)
        if not end_date:
            end_date = datetime.date.today() - datetime.timedelta(days=1)

        if start_date:
            try:
                start_date = datetime.datetime.strptime(start_date, '%d/%m/%Y')
            except ValueError:
                return Response(status=HTTP_400_BAD_REQUEST)
        if not start_date:
            start_date = end_date - datetime.timedelta(days=4)

        diff_date = end_date - start_date
        if diff_date.days >= 5:
            return Response(status=HTTP_400_BAD_REQUEST,
                            data={ 'msg': ('O período selecionado não '
                                               'pode ultrapassar o intervalo '
                                               'de 5 dias.') })
        elif diff_date.days < 0:
            return Response(status=HTTP_400_BAD_REQUEST,
                            data={ 'msg': ('Data final (end_date) deve '
                                               'ser maior que a data inicial '
                                               '(start_date).') })

        # query two days before, so we can use to fill non business days 
        query_start_date = start_date - datetime.timedelta(days=2)
        rates = CurrencyRate.objects.filter(
            date__range=[query_start_date, end_date])

        # Construct the result, as we need to fill correctly non business days
        result = []
        i_date = start_date
        while i_date <= end_date:
            # Get the first rate before today, if there is no today rate
            rate = rates.filter(date__lte=i_date).order_by('-date').first()
            if rate:
                result.append({
                    'id': rate.id,
                    'date': i_date.strftime('%d/%m/%Y'),
                    'base': rate.base,
                    'rates': json.loads(rate.rates)
                })
            i_date = i_date + datetime.timedelta(days=1)
        return Response(status=HTTP_200_OK, data=result)

