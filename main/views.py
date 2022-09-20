from rest_framework.views import APIView
from django.http import JsonResponse
from .models import MailingList, Client
from .serializers import MailingListSerializer, ClientSerializer, MessageSerializer
from django.core import serializers

from .tasks import sendMessageTask

from datetime import datetime
from pytz import timezone
from django.utils import timezone
from notifserv.settings import TIME_ZONE

class Clients(APIView):

    def post(self, request):

        serializer = ClientSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'successfully created new client', 'object': serializer.data})

        return JsonResponse({'message': 'failed to create new client', 'object': serializer.data, 'error': serializer.errors})

    def patch(self, request):
        client = Client.objects.get(pk=request.data.get('id'))

        serializer = ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return JsonResponse({'message': 'successfully updated the client', 'object': serializer.data})

        return JsonResponse({'message': 'failed to update the client', 'object': serializer.data, 'error': serializer.errors})

    def delete(self, request):
        client = Client.objects.get(pk=request.data.get('id'))
        client.delete()

        serializer = ClientSerializer(client)

        return JsonResponse({'message': 'successfully deleted the client', 'object': serializer.data})


class MailingLists(APIView):

    # dtfmt = '%Y-%m-%dT%H:%M:%S %z'

    def scheduleMailings(self, data):

        mailinglist = MailingList.objects.get(pk=data['id'])
        if isinstance(mailinglist.fltr, int):
            clients = Client.objects.filter(operCode=mailinglist.fltr)
        else:
            clients = Client.objects.filter(tag=mailinglist.fltr)
        

        for client in clients:
            
            startDT = mailinglist.startDatetime
            expDT = mailinglist.expDatetime

            if client.tz != TIME_ZONE:
                startDT = startDT.astimezone(timezone(client.tz))
                expDT = expDT.astimezone(timezone(client.tz))

            if startDT < timezone.now() < expDT:
                sendMessageTask.apply_async(
                    args=[mailinglist.id, client.id, client.phoneNumber, mailinglist.text],
                    expires=expDT
                )

            else:
                sendMessageTask.apply_async(
                    args=[mailinglist.id, client.id, client.phoneNumber, mailinglist.text],
                    eta=startDT,
                    expires=expDT
                )

    def post(self, request):
        
        serializer = MailingListSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            self.scheduleMailings(serializer.data)

            return JsonResponse({'message': 'successfully created new mailing list', 'object': serializer.data})

        return JsonResponse({'message': 'failed to create new mailing list', 'object': serializer.data, 'error': serializer.errors})



#     def put(self, request):

#     def delete(self, request):


# class GeneralStat(APIView):
#     def get(self, request):



# class DetailedStat(APIView):
#     def get(self, request):

