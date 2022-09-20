from dataclasses import fields
from rest_framework import serializers
from .models import MailingList, Client, Message


class MailingListSerializer(serializers.ModelSerializer):
    class Meta:
        model = MailingList
        fields = ('__all__')


class ClientSerializer(serializers.ModelSerializer):

    def update(self, instance, validated_data):
        instance.phoneNumber = validated_data.get('phoneNumber', instance.phoneNumber)
        instance.operCode = validated_data.get('operCode', instance.operCode)
        instance.tag = validated_data.get('tag', instance.tag)
        instance.tz = validated_data.get('tz', instance.tz)
        instance.save()
        return instance

    class Meta:
        model = Client
        fields = ('__all__')


class MessageSerializer(serializers.ModelSerializer):

    # mailinglist = serializers.PrimaryKeyRelatedField(read_only=False, queryset=MailingList.objects.all())
    # client = serializers.PrimaryKeyRelatedField(read_only=False, queryset=Client.objects.all())

    # mailinglist = MailingListSerializer()
    # client = ClientSerializer()

    def create(self, validated_data):
        return Message.objects.create(**validated_data)

    class Meta:
        model = Message
        fields = ('__all__')
        # fields = ('sendDatetime', 'status', 'mailinglist', 'client')
