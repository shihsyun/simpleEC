import json
from django.test import TestCase
from django.contrib.auth.models import Group, Permission
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.status import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND)
from .models import Product


class ProductTestCase(APITestCase):

    def setUp(self):
        self.email = 'test1@test.com'
        self.password = 'Foo001'
        self.url = ''
        self.token = ''

        per = Permission.objects.get(name='onlyread')
        group, _ = Group.objects.get_or_create(name='Customer')
        per = Permission.objects.get(name='can_create')
        group.permissions.add(per)
        group, _ = Group.objects.get_or_create(name='Seller')

        user_data = {
            "email": self.email,
            "password": self.password
        }
        self.url = reverse('customer_register')
        response = self.client.post(self.url, user_data)

        self.url = reverse('customer_verify_gencode')
        token = self.client.post(
            self.url, {'email': self.email})
        self.url = reverse('customer_verifycode')
        response = self.client.get(
            self.url, {'token': str(token.content.decode('utf-8'))})

        self.url = reverse('customer_login')
        response = self.client.post(self.url, {'username': self.email,
                                               'password': self.password}, format='json')

        self.token = json.loads(response.content)['token']
        self.client.credentials(HTTP_AUTHORIZATION='token '+self.token)
        self.url = reverse('seller_apply')
        response = self.client.put(self.url, {'email': self.email,
                                              'password': self.password}, format='json')
        self.assertEqual(str(HTTP_204_NO_CONTENT),
                         response.content.decode('utf-8'))

    def test_create_product(self):

        product_data = {
            "title": "test Echo",
            "sku": "Foo001",
            "price": 123.45,
            "description": "test123",
            "available": "true",
            "stock": 30
        }

        self.url = reverse('products')
        self.client.credentials(HTTP_AUTHORIZATION='token '+self.token)
        response = self.client.post(self.url, product_data)

        self.assertEqual(HTTP_201_CREATED, response.status_code)
        self.assertTrue('sku' in json.loads(response.content))

    def test_destory_product(self):
        self.test_create_product()
        product = Product.objects.get(sku='Foo001')
        print(product.id)
        self.url = reverse('product', kwargs={'pk': product.id})
        self.client.credentials(HTTP_AUTHORIZATION='token '+self.token)
        response = self.client.delete(self.url)
        self.assertEqual(HTTP_204_NO_CONTENT, response.status_code)
