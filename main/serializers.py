from dataclasses import fields
from rest_framework import serializers
from .models import MailingList, Client, Message


class MailingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailingList
        fields = ('__all__')


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('__all__')


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ('__all__')
