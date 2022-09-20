import requests
from django.utils import timezone
from celery import shared_task
from .serializers import MessageSerializer


URL = f'https://google.com'
HEADERS = {'Content-Type': 'application/json'}

@shared_task
def sendMessageTask(mailinglist, client, phoneNumber, text):
    data = {
        'sendDatetime': timezone.now(),
        'status': -1,
        'mailinglist_id': mailinglist,
        'client_id': client
    }
    serializer = MessageSerializer(data=data)
    if serializer.is_valid():
        instance = serializer.save()

        r = requests.post(
            URL,
            headers=HEADERS,
            json={
                'id': serializer.data['id'],
                'phone': phoneNumber,
                'text': text
            }
        )
        instance.status = r.json()['code']
        instance.save()
