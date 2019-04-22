import json
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
# from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
# from rest_framework.test import APIClient
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND)


"""
Let's take a test-first approach.
"""


class CustomerRegisterTestCase(APITestCase):

    def setUp(self):
        self.email = "test1@test.com"
        self.password = "foo"
        self.url = ""

    def test_post(self):
        user_data = {
            "email": self.email,
            "password": self.password
        }
        self.url = reverse('customer_register')
        response = self.client.post(self.url, user_data)
        self.assertEqual(HTTP_201_CREATED, response.status_code)
        self.assertTrue('email' in json.loads(response.content))

    def test_login_notactiveuser(self):

        self.test_post()

        self.url = reverse('customer_login')
        response = self.client.post(self.url, {'username': self.email,
                                               'password': self.password}, format='json')
        self.assertEqual(HTTP_404_NOT_FOUND, response.status_code)

    def test_activeuser(self):

        self.test_post()

        self.url = reverse('customer_verify_gencode')
        token = self.client.post(
            self.url, {'email': self.email})
        self.url = reverse('customer_verifycode')
        response = self.client.get(
            self.url, {'token': str(token.content.decode('utf-8'))})
        self.assertEqual(HTTP_200_OK, response.status_code)
        self.assertEqual(str(HTTP_204_NO_CONTENT),
                         response.content.decode('utf-8'))

    def test_login_activeuser(self):
        self.test_activeuser()
        self.url = reverse('customer_login')
        response = self.client.post(self.url, {'username': self.email,
                                               'password': self.password}, format='json')
        self.assertEqual(HTTP_200_OK, response.status_code)
        self.assertTrue('token' in json.loads(response.content))

    def test_logout_withnovalidatetoken(self):
        self.test_activeuser()
        self.url = reverse('customer_logout')
        response = self.client.post(
            self.url, {'username': self.email}, format='json')
        self.assertEqual(HTTP_401_UNAUTHORIZED, response.status_code)

    def test_logout(self):

        self.test_activeuser()
        self.url = reverse('customer_login')
        response = self.client.post(self.url, {'username': self.email,
                                               'password': self.password}, format='json')
        token = json.loads(response.content)['token']
        self.url = reverse('customer_logout')
        self.client.credentials(HTTP_AUTHORIZATION='token '+token)
        response = self.client.post(
            self.url, {'username': self.email}, format='json')
        self.assertEqual(HTTP_200_OK, response.status_code)
        self.assertEqual(str(HTTP_204_NO_CONTENT),
                         response.content.decode('utf-8'))


class CustomerManagerTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        email = 'user@test.com'
        password = 'foo'
        user = User.objects.create(email=email, password=password)
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertFalse(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

        try:
            self.assertIsNone(user.username)
        except AttributeError:
            pass

        with self.assertRaises(TypeError):
            User.objects.create()

        with self.assertRaises(TypeError):
            User.objects.create(email='')

        with self.assertRaises(ValueError):
            User.objects.create(email='', password=password)
