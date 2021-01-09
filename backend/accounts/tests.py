from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from .models import CustomUser
from .serializers import UserSerializer


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

    def test_create_duplicate_username_or_email(self):
        payload = self.account_data_1
        response_1 = self.clinet.post(self.endpoint, data=payload)
        response_2 = self.clinet.post(self.endpoint, data=payload)
        self.assertEqual(response_2.status_code, status.HTTP_401_UNAUTHORIZED)


class ViewAccountTest(APITestCase):
    def setUp(self):
        self.all_endpoint = reverse('users_all')
        self.one_endpoint = reverse('users_details')
        self.account_data_1 = {
            'username': 'test_user_1',
            'email': "user1@test.mail.com",
            'password': 'TestPassword1'
        }
        self.account_data_2 = {
            'username': 'test_user_2',
            'email': "user2@test.mail.com",
            'password': 'TestPassword2'
        }
        user_serializer = UserSerializer(data=self.account_data_1)
        if user_serializer.is_valid():
            user_serializer.save()
        user_serializer = UserSerializer(data=self.account_data_2)
        if user_serializer.is_valid():
            user_serializer.save()

    def test_show_all_users(self):
        payload = {}
        response = self.client.get(self.all_endpoint, data=payload)
        self.assertEqual(len(response.data), 2)
    
    def test_show_user_details(self):
        payloard = {}

    def test_modify_user_details(self):
        pass

    def test_delete_user(self):
        pass

    def test_view_all_post_by_user(self):
        pass

    def test_view_all_group_with_user(self):
        pass

    def test_view_all_review_with_user(self):
        pass
