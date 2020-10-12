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
        self.assertEqual(calculate_new_clients(Client.objects), 25.0)

        Client.objects.create(created_by=self.user, number=2, total=100.0)
        self.assertEqual(calculate_new_clients(Client.objects), 145.0)

        # Add 10 clients with 75 PLN TOTAL, AMOUNT OF CLIENTS: 12
        # First client with amount of 50, now become worth 40 instead of 25
        Client.objects.bulk_create([Client(created_by=self.user,number=x,total=80.0) for x in range(3,13)])
        self.assertEqual(calculate_new_clients(Client.objects), 960.0)

    def testProfitFromOldClientsWithoutPremium(self):
        obj = Client.objects.create(created_by=self.user, number=1, total=25.00, core=15.00) # total - 1 prog, 
        self.assertEqual(calculate_old_clients(Client.objects), float(obj.total)*1.7)

        Client.objects.filter(pk=obj.pk).update(core=21.00)
        obj.refresh_from_db()
        self.assertEqual(calculate_old_clients(Client.objects), float(obj.total)*1.8)

        Client.objects.filter(pk=obj.pk).update(core=5.00)
        obj.refresh_from_db()
        self.assertEqual(calculate_old_clients(Client.objects), float(obj.total)*1.5+3)

        Client.objects.filter(pk=obj.pk).update(total=30.00)
        obj.refresh_from_db()
        self.assertEqual(calculate_old_clients(Client.objects), float(obj.total)*1.7+3)

        Client.objects.filter(pk=obj.pk).update(core=15.00)
        obj.refresh_from_db()
        self.assertEqual(calculate_old_clients(Client.objects), float(obj.total)*1.8)

        Client.objects.filter(pk=obj.pk).update(core=21.00)
        obj.refresh_from_db()
        self.assertEqual(calculate_old_clients(Client.objects), float(obj.total)*2.0)

    def testProfitFromOldClientWithPremium(self):
        obj = Client.objects.create(created_by=self.user, number=1, total=25.00, core=15.00, premium=10.00) # total - 1 prog, 
        self.assertEqual(calculate_old_clients(Client.objects), float(obj.total)*1.7+10.00)

        Client.objects.filter(pk=obj.pk).update(premium=15.00)
        obj.refresh_from_db()
        self.assertEqual(calculate_old_clients(Client.objects), float(obj.total)*1.7+15.0*1.4)

        Client.objects.filter(pk=obj.pk).update(premium=30.00)
        obj.refresh_from_db()
        self.assertEqual(calculate_old_clients(Client.objects), float(obj.total)*1.7+30.0*1.8)



