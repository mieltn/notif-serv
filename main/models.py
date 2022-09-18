from django.db import models


class MailingList(models.Model):
    sendDatetime = models.DateTimeField()
    text = models.CharField(max_length=500)
    fltr = models.CharField(max_length=50)
    endDatetime = models.DateTimeField()


class Client(models.Model):
    phoneNumber = models.BigIntegerField()
    operCode = models.IntegerField()
    tag = models.CharField(max_length=20)
    tz = models.CharField(max_length=40)


class Message(models.Model):
    sendDatetime = models.DateTimeField()
    status = models.CharField(max_length=30)
    mailinglist = models.ForeignKey(MailingList, on_delete=models.CASCADE)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)