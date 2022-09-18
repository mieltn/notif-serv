from rest_framework.views import APIView
from django.http import JsonResponse
from .models import MailingList, Client, Message
from .serializers import MailingListSerializer, ClientSerializer, MessageSerializer

class Clients(APIView):

    def post(self, request):
        data = {
            'phoneNumber': request.data.get('phoneNumber'),
            'operCode': request.data.get('operCode'),
            'tag': request.data.get('tag'),
            'tz': request.data.get('tz')
        }
        serializer = ClientSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'successfully created new client', 'object': data})

        return JsonResponse({'message': 'failed to create new client', 'object': data, 'error': serializer.errors})

    def put(self, request):
        client = Client.objects.get(pk=request.data.get('id'))

        client.phoneNumber = request.data.get('phoneNumber', client.phoneNumber)
        client.operCode = request.data.get('operCode', client.operCode)
        client.tag = request.data.get('tag', client.tag)
        client.tz = request.data.get('tz', client.tz)

        client.save()

        serializer = ClientSerializer(client)

        return JsonResponse({'message': 'successfully updated the client', 'object': serializer.data})

    def delete(self, request):
        client = Client.objects.get(pk=request.data.get('id'))
        client.delete()

        serializer = ClientSerializer(client)

        return JsonResponse({'message': 'successfully deleted the client', 'object': serializer.data})


class MailingLists(APIView):

    def post(self, request):

    def put(self, request):

    def delete(self, request):


class GeneralStat(APIView):


class DetailedStat(APIView):


class SendMessages(APIView):
    