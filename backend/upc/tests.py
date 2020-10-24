import json
from datetime import timedelta
from django.utils import timezone
from time import sleep

from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from upc.utils import calculate_new_clients, calculate_old_clients
from upc.serializers import ClientSerializer
from conf.utility import prevent_request_warnings


from upc.models import Client, TypeOfClient


class UpcClientTestCase(APITestCase):
    
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="test", password="st3ong-Pssw1d")
        self.client.force_authenticate(user=self.user) # bypass authentication 

    def testListClientsForCurrentMonth(self):
        Client.objects.bulk_create([
            Client(created_by=self.user, number=1111, total=125.22),
            Client(created_by=self.user, number=1112, total=221.22),
            Client(created_by=self.user, number=1113, total=222.22),
            Client(created_by=self.user, number=1114, total=55.21, created_on=timezone.now()-timedelta(weeks=5))]
            )

        response = self.client.get(reverse('list_clients'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def testListClientsForMultipleUsers(self):
        test_user = get_user_model().objects.create_user(username="test2", password="st3ong-Pssw1d")

        Client.objects.bulk_create([
            Client(created_by=self.user, number=1111, total=122.11),
            Client(created_by=test_user, number=1112, total=212.22)
        ])

        response = self.client.get(reverse('list_clients'))
        self.assertEqual(len(response.data), 1)
    

    def testProfitFromNewClients(self):
        Client.objects.create(created_by=self.user, number=1, total=50.0)
        self.assertEqual(calculate_new_clients(Client.objects)[0], 25.0)

        Client.objects.create(created_by=self.user, number=2, total=100.0)
        self.assertEqual(calculate_new_clients(Client.objects)[0], 145.0)

        # Add 10 clients with 75 PLN TOTAL, AMOUNT OF CLIENTS: 12
        # First client with amount of 50, now become worth 40 instead of 25
        Client.objects.bulk_create([Client(created_by=self.user,number=x,total=80.0) for x in range(3,13)])
        self.assertEqual(calculate_new_clients(Client.objects)[0], 960.0)

    def testProfitFromOldClientsWithoutPremium(self):
        obj = Client.objects.create(created_by=self.user, number=1, total=25.00, core=15.00) # total - 1 prog, 
        self.assertEqual(calculate_old_clients(Client.objects)[0], float(obj.total)*1.7)

        Client.objects.filter(pk=obj.pk).update(core=21.00)
        obj.refresh_from_db()
        self.assertEqual(calculate_old_clients(Client.objects)[0], float(obj.total)*1.8)

        Client.objects.filter(pk=obj.pk).update(core=5.00)
        obj.refresh_from_db()
        self.assertEqual(calculate_old_clients(Client.objects)[0], float(obj.total)*1.5+3)

        Client.objects.filter(pk=obj.pk).update(total=30.00)
        obj.refresh_from_db()
        self.assertEqual(calculate_old_clients(Client.objects)[0], float(obj.total)*1.7+3)

        Client.objects.filter(pk=obj.pk).update(core=15.00)
        obj.refresh_from_db()
        self.assertEqual(calculate_old_clients(Client.objects)[0], float(obj.total)*1.8)

        Client.objects.filter(pk=obj.pk).update(core=21.00)
        obj.refresh_from_db()
        self.assertEqual(calculate_old_clients(Client.objects)[0], float(obj.total)*2.0)

    def testProfitFromOldClientWithPremium(self):
        obj = Client.objects.create(created_by=self.user, number=1, total=25.00, core=15.00, premium=10.00)
        self.assertEqual(calculate_old_clients(Client.objects)[0], float(obj.total)*1.7+10.00)

        Client.objects.filter(pk=obj.pk).update(premium=15.00)
        obj.refresh_from_db()
        self.assertEqual(calculate_old_clients(Client.objects)[0], float(obj.total)*1.7+15.0*1.4)

        Client.objects.filter(pk=obj.pk).update(premium=30.00)
        obj.refresh_from_db()
        self.assertEqual(calculate_old_clients(Client.objects)[0], float(obj.total)*1.7+30.0*1.8)

        

    def testProfitFromMultipleClients(self):
        Client.objects.create(created_by=self.user, number=1, total=50.0)
        Client.objects.create(created_by=self.user, number=2, total=100.0)
        Client.objects.bulk_create([Client(created_by=self.user,number=x,total=80.0) for x in range(3,13)])
        Client.objects.create(type=TypeOfClient.PRESENT, created_by=self.user, number=1, total=25.00, core=15.00) # + 42.5 
        Client.objects.create(type=TypeOfClient.PRESENT, created_by=self.user, number=1, total=30.00, core=5.00) # + 54.0

        response = self.client.get(reverse('profit'))
        self.assertEqual(response.data['Profit']['New'], 960.0)
        self.assertEqual(response.data['Profit']['Old'], 96.5)
        self.assertEqual(response.data['Total'], 1056.5)

    def testProfitFromMultipleUsers(self):
        test_user = get_user_model().objects.create_user(username="test2", password="st3ong-Pssw1d")

        Client.objects.create(created_by=self.user, number=1, total=50.0)
        Client.objects.create(created_by=self.user, number=2, total=100.0)
        Client.objects.bulk_create([Client(created_by=self.user,number=x,total=80.0) for x in range(3,13)])
        Client.objects.create(type=TypeOfClient.PRESENT, created_by=self.user, number=1, total=25.00, core=15.00) # + 42.5 
        Client.objects.create(type=TypeOfClient.PRESENT, created_by=self.user, number=1, total=30.00, core=5.00) # + 54.0

        Client.objects.create(created_by=test_user, number=1, total=50.0)
        Client.objects.create(created_by=test_user, number=2, total=100.0)
        Client.objects.bulk_create([Client(created_by=test_user,number=x,total=80.0) for x in range(3,13)])
        Client.objects.create(type=TypeOfClient.PRESENT, created_by=test_user, number=1, total=25.00, core=15.00) # + 42.5 

        response = self.client.get(reverse('profit'))
        self.assertEqual(response.data['Total'], 1056.5)

        self.client.force_authenticate(user=test_user)
        response = self.client.get(reverse('profit'))
        self.assertEqual(response.data['Total'], 1002.5)


    def testUpdateAndRemoveExisitngClient(self):
        client = Client.objects.create(created_by=self.user, number=1, total=50.0)
        response = self.client.patch(reverse('client_detail_view', kwargs={'pk': client.id}), {'total': 25.0})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        serialized = ClientSerializer(client).data
        data = {
            'number': serialized.get('number'),
            'type': serialized.get('type'),
            'total': 30.0
        }

        response = self.client.put(reverse('client_detail_view', kwargs={'pk': client.id}), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.get(reverse('client_detail_view', kwargs={'pk': client.id}))
        self.assertEqual(response.data['id'], client.id)
        self.assertEqual(float(response.data['total']), 30.00)

        response = self.client.delete(reverse('client_detail_view', kwargs={'pk': client.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(reverse('list_clients'))
        self.assertEqual(len(response.data), 0)

    @prevent_request_warnings
    def testCannotDeleteDifferentUserClient(self):
        test_user = get_user_model().objects.create_user(username="test2", password="st3ong-Pssw1d")
        client = Client.objects.create(created_by=test_user, number=1, total=50.0)

        # self.client is authorized with different user
        response = self.client.delete(reverse('client_detail_view', kwargs={'pk': client.id}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


