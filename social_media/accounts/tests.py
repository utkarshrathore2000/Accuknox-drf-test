from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()

class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.signup_url = '/auth/sign-up/'
        self.login_url = '/auth/api/token/'
        self.user_data = {
            'email': 'test@example.com',
            'password': 'testpassword',
            'first_name': "test",
            'last_name': "test_last"
        }

    def test_signup(self):
        response = self.client.post(self.signup_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().email, 'test@example.com')
        self.assertTrue('refresh' in response.data)
        self.assertTrue('access' in response.data)

    def test_login(self):
        # First, create a user
        self.client.post(self.signup_url, self.user_data, format='json')

        # Now, try to login with the created user
        response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('refresh' in response.data)
        self.assertTrue('access' in response.data)
