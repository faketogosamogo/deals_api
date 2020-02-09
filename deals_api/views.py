import csv
from django.db.models import Sum, Q
import django.utils.datastructures
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.cache import cache_page
from . import models


class DealViewSet(viewsets.ModelViewSet):
    @api_view(['GET'])
    @cache_page(60 * 15)
    def get_deals(request):
        deals = models.Deal.objects.values('customer').annotate(dcount=Sum('total')).order_by('-dcount')[0:5]
        clients = []
        usernames = []

        for deal in deals:
            usernames.append(deal['customer'])

        for deal in deals:
            gems = models.Deal.objects.filter(customer=deal['customer']).values('item').distinct()
            gems_list = []
            for gem in gems:
                for username in usernames:
                    if deal['customer'] == username:
                        continue
                    count = models.Deal.objects.filter(Q(customer=username) & Q(item=gem['item'])).count()
                    if count>0:
                        gems_list.append(gem['item'])

            client = models.Client()
            client.username = deal['customer']
            client.spent_money = deal['dcount']
            client.gems = gems_list
            clients.append(client)
        clientschema = models.Client()
        return Response(clientschema.dump(clients, many=True))

    @api_view(['POST'])
    def upload_csv_deals(request):
        try:
            file = request.FILES['deals.csv']
            decoded_file = file.read().decode('utf-8').splitlines()
            reader = csv.reader(decoded_file)
        except UnicodeDecodeError:
            return Response('Ошибка чтения файла', status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        except django.utils.datastructures.MultiValueDictKeyError:
            return Response('Файл не был передан', status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            

        deals = []
        try:
            next(reader)
            for deal in reader:
                deals.append(models.Deal(customer=deal[0],
                                           item=deal[1],
                                           total=deal[2],
                                           quantity=deal[3],
                                           date=deal[4]))
        except csv.Error:
            return Response("Ошибка чтения csv файла!",status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        models.Deal.objects.all().delete()
        models.Deal.objects.bulk_create(deals)

        return Response(status=status.HTTP_200_OK)

