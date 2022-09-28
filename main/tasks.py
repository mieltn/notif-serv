import requests
from django.utils import timezone
from celery import shared_task
from .models import Client, MailingList
from .serializers import MessageSerializer

from notifserv.settings import TIME_ZONE

URL = f'https://google.com'
HEADERS = {'Content-Type': 'application/json'}


@shared_task
def scheduleMailingTask(data):

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


@shared_task
def sendMessageTask(mailinglist, client, phoneNumber, text):
    data = {
        'sendDatetime': timezone.now(),
        'status': -1,
        'mailinglist': mailinglist,
        'client': client
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
        # instance.status = r.json()['code']
        instance.status = r.status_code
        instance.save()
        return serializer.data

    return serializer.errors
