from django.contrib import admin
from .models import MailingList, Client, Message

admin.site.register(MailingList)
admin.site.register(Client)
admin.site.register(Message)