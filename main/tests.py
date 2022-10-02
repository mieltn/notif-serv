from django import test
from rest_framework import status
from django.urls import reverse
from .models import Client

client = test.Client()

class ClientCreateTest(test.TestCase):

    def setUp(self):
        self.valid_data = {
            "phoneNumber": 73334445566,
            "operCode": 333,
            "tag": "xxx",
            "tz": "Asia/Tashkent"
        }

        self.invalid_data = {
            "phoneNumber": None,
            "operCode": 333,
            "tag": "xxx",
            "tz": "Asia/Tashkent"
        }


    def testValidCreate(self):
        response = client.post(
            reverse('clients'),
            self.valid_data,
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def testInvalidCreate(self):
        response = client.post(
            reverse('clients'),
            self.invalid_data,
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class ClientUpdateTest(test.TestCase):

    def setUp(self):
        self.cl = Client.objects.create(
            phoneNumber = 79629583294,
            operCode = 962,
            tag = 'xxx',
            tz = 'Asia/Tashkent'
        )
        self.valid_data = {
            "phoneNumber": 79999583294,
            "operCode": 999
        }
        self.invalid_data = {
            "phoneNumber": "my phone",
            "operCode": 999
        }


    def testValidUpdate(self):
        response = client.patch(
            reverse('client', kwargs = {'id': self.cl.id}),
            self.valid_data,
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def testInvalidUpdate(self):
        response = client.patch(
            reverse('client', kwargs = {'id': self.cl.id}),
            self.invalid_data,
            content_type = 'application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        
class ClientDeleteTest(test.TestCase):

    def setUp(self):
        self.cl = Client.objects.create(
            phoneNumber = 79629583294,
            operCode = 962,
            tag = 'xxx',
            tz = 'Asia/Tashkent'
        )

    def testDelete(self):
        response = client.delete(
            reverse('client', kwargs = {'id': self.cl.id})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
