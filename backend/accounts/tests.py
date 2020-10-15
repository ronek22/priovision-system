import json

from django.contrib.auth import get_user_model
from django.urls import reverse
from conf.utility import prevent_request_warnings
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from time import sleep


class AccountTestCase(APITestCase):

    profile_url = reverse("profile")
    username = "testuser"
    password = "strong_pass1wrd"

    def setUp(self):
        self.user = get_user_model().objects.create_user(username=self.username, password=self.password)

    def test_login(self):
        data = {"username": self.username, "password": self.password}
        resp = self.client.post(reverse('login'), data)
        self.assertEquals(resp.status_code, status.HTTP_200_OK)
        self.assertEquals(resp.data['user']['username'], self.username)
        self.assertIsNotNone(resp.data['access_token'])
        self.assertIsNotNone(resp.cookies['csrftoken'])
        self.assertIsNotNone(resp.cookies['refreshtoken'])

    @prevent_request_warnings
    def test_cant_create_user_with_the_same_username(self):
        data = {"username": self.username, "password": self.password}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration(self):
        data = {"username": "registartion_user", "email": "test@domain.com", "password": "strong_pass1wrddsa"}
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    @prevent_request_warnings
    def test_get_profile_unauthorized(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_profile_authorized(self):
        data = {"username": self.username, "password": self.password}
        resp = self.client.post(reverse('login'),data)

        self.client.credentials(HTTP_AUTHORIZATION=f"Token {resp.data['access_token']}")
        resp = self.client.get(self.profile_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)

    def test_get_new_access_token_using_refresh_token(self):
        data = {"username": self.username, "password": self.password}
        resp = self.client.post(reverse('login'),data)
        old_access_token = resp.data['access_token']

        sleep(1)

        resp = self.client.post(reverse('refresh'))
        self.assertNotEqual(old_access_token, resp.data['access_token'])

    @prevent_request_warnings
    def test_validate_username(self):
        resp = self.client.post(reverse('validate-username'), {'username': self.username})
        self.assertFalse(resp.data['available'])

        resp = self.client.post(reverse('validate-username'), {'username': 'noexisteduser'})
        self.assertTrue(resp.data['available'])

        resp = self.client.post(reverse('validate-username'))
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(resp.data['error'], 'Invalid username')





    