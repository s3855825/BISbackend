# Create your tests here.
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status


class CreateAccountTest(APITestCase):
    def setUp(self):
        self.endpoint = reverse('users_all')

        self.account_data_1 = {
            'username': 'test_user_1',
            'email': "user1@test.mail.com",
            'password': 'TestPassword1'
        }

    def test_create_accounts(self):
        payload = self.account_data_1
        response = self.client.post(self.endpoint, data=payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_duplicate_username(self):
        pass
