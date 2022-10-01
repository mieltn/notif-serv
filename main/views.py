from rest_framework.views import APIView
from django.http import JsonResponse
from django.db.models import Count

from .models import MailingList, Client
from .serializers import MailingListSerializer, ClientSerializer
# from django.core import serializers

from notifserv.celery import app

from .tasks import scheduleMailingTask

# from datetime import datetime
# from pytz import timezone
# from django.utils import timezone


class Clients(APIView):

    def post(self, request):

        serializer = ClientSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'successfully created new client', 'object': serializer.data})

        return JsonResponse({'message': 'failed to create new client', 'object': serializer.data, 'error': serializer.errors})

    def patch(self, request, id):
        client = Client.objects.get(pk=id)

        serializer = ClientSerializer(client, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            return JsonResponse({'message': 'successfully updated the client', 'object': serializer.data})

        return JsonResponse({'message': 'failed to update the client', 'object': serializer.data, 'error': serializer.errors})

    def delete(self, request, id):
        client = Client.objects.get(pk=id)
        client.delete()

        serializer = ClientSerializer(client)

        return JsonResponse({'message': 'successfully deleted the client', 'object': serializer.data})


class MailingLists(APIView):

    def post(self, request):
        
        serializer = MailingListSerializer(data=request.data, partial=True)

        if serializer.is_valid():
            mailinglist = serializer.save()

            tresp = scheduleMailingTask.apply_async(
                args=[serializer.data],
                eta = mailinglist.startDatetime,
                expires = mailinglist.expDatetime
            )

            mailinglist.taskId = tresp.id
            mailinglist.save()

            return JsonResponse({'message': 'successfully created new mailing list', 'object': serializer.data})

        return JsonResponse({'message': 'failed to create new mailing list', 'object': serializer.data, 'error': serializer.errors})


    def patch(self, request, id):
        mailinglist = MailingList.objects.get(pk=id)

        serializer = MailingListSerializer(mailinglist, data=request.data, partial=True)
        if serializer.is_valid():
            app.control.revoke(mailinglist.taskId, terminate=True)

            mailinglist = serializer.save()

            tresp = scheduleMailingTask.apply_async(
                args=[serializer.data],
                eta = mailinglist.startDatetime,
                expires = mailinglist.expDatetime
            )
            mailinglist.taskId = tresp.id
            mailinglist.save()

            return JsonResponse({'message': 'successfully updated the mailing list', 'object': serializer.data})

        return JsonResponse({'message': 'failed to update the mailing list', 'object': serializer.data, 'error': serializer.errors})
            

    def delete(self, request, id):
        mailinglist = MailingList.objects.get(pk=id)
        app.control.revoke(mailinglist.taskId, terminate=True)
        mailinglist.delete()

        serializer = MailingListSerializer(mailinglist)

        return JsonResponse({'message': 'successfully deleted the mailing list', 'object': serializer.data})



class GeneralStat(APIView):
    def get(self, request):
        stat = {}
        mailings = MailingList.objects.all()
        stat['total number of mailings'] = mailings.count()

        for mailing in mailings:
            messages = mailing.message_set.select_related()
            msStat = list(messages.values('status').annotate(messagesSent=Count('id')))
            stat[mailing.id] = msStat

        return JsonResponse({'message': 'General statistics about mailings and messages sent by status', 'data': stat})


# class DetailedStat(APIView):
#     def get(self, request):

