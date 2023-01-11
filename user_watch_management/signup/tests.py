import json
from typing import Optional
from unittest import mock
from uuid import uuid4
from django.test import TestCase

from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from alerts.constants import ALERT_NOT_UPDATED_MESSAGE


class TestSignupV1New(TestCase):
    test_url = "/signup/v1/new"

    def setUp(self) -> None:
        self.maxDiff = None
        self.client = APIClient()

        return super().setUp()

    def test_signup_v1_new(self):
        username = "test_email@test.com"

        response = self.client.post("/signup/v1/new", data={"username": username, "password": "test_password"})

        # Assert the API response
        self.assertEqual(response.status_code, 201)

        content = json.loads(response.content)
        self.assertEqual(content, {})

        # Assert the user was created
        self.assertTrue(User.objects.filter(username=username, email=username).exists())
