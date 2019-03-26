#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model

try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse

from faker import Faker
from rest_framework.test import APITestCase
from rest_framework import status

fake = Faker()


class TestRatingsAPI(APITestCase):

    def setUp(self):
        username = fake.user_name()
        email = fake.email()
        password = fake.password()
        self.user = get_user_model().objects.create(username=username, email=email)
        self.user.set_password(password)
        self.user.save()
        self.client.login(
            username=self.user.username,
            password=password)

    def test_rating_api_get_request_not_allowed(self):
        # Data
        url = reverse('ratings:api:create')

        # Do action
        response = self.client.get(url, format='json')

        # Asserts
        self.assertTrue(status.is_client_error(response.status_code))

    def test_skip_api_get_request_not_allowed(self):
        # Data
        url = reverse('ratings:api:skip')

        # Do action
        response = self.client.get(url, format='json')

        # Asserts
        self.assertTrue(status.is_client_error(response.status_code))
