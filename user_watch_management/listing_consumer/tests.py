from typing import Optional
from uuid import uuid4
from django.test import TestCase
from rest_framework.test import APIClient

from unittest import mock
from django.test import TestCase
from django.contrib.auth.models import User
from django.core import mail


from listing_consumer.serializers import KennyUPullListingSerializer
from listing_consumer.tasks import ingest_listening
from alerts.models import Alert, Vehicle
from alerts.models import Alert


class NewListingTests(TestCase):
    test_url = "/listing-consumer/v1/new-listing"

    def setUp(self) -> None:
        self.maxDiff = None
        self.client = APIClient()

        return super().setUp()

    @mock.patch("listing_consumer.tasks.ingest_listening")
    def test_new_listing(self, *args):
        body = {
            "make": "Honda",
            "model": "Civic",
            "year": "2000",
            "date_listed": "2020-01-01",
            "row_id": "A12",
            "branch": "Ottawa",
            "listing_url": "https://www.kennyupull.com/listing/A12",
            "client_id": "1234",
        }

        response = self.client.post(self.test_url, body, format="json")

        self.assertEqual(response.status_code, 204)

    @mock.patch("listing_consumer.serializers.KennyUPullListingSerializer.is_valid", return_value=False)
    @mock.patch.object(KennyUPullListingSerializer, "errors", {"non_field_errors": ["Invalid data."]})
    def test_new_listing_invalid_body(self, *args):
        body = {
            "make": "Honda",
            "model": "Civic",
            "year": "2000",
            "date_listed": "2020-01-01",
            "row_id": "A12",
            "branch": "Ottawa",
            "listing_url": "https://www.kennyupull.com/listing/A12",
            "client_id": "1234",
            "invalid_field": "invalid",
        }

        response = self.client.post(self.test_url, body, format="json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"non_field_errors": ["Invalid data."]})


class IngestListingTests(TestCase):
    def setUp(self) -> None:
        self.maxDiff = None
        username_and_email = "tester@test.com"
        self.user = User.objects.create_user(username_and_email, username_and_email, password=str(uuid4()))

        return super().setUp()

    def __set_up_an_alert(self, user: Optional[User] = None, branch: Optional[str] = None) -> Alert:
        manufacturer_name = "Toyota"
        model_name = "Corolla"
        model_year = "1996"

        vehicle = Vehicle.objects.create(manufacturer_name=manufacturer_name, model_year=model_year, model_name=model_name)
        user = user if user else self.user

        return Alert.objects.create(user=user, vehicle=vehicle, branch=branch)

    def test_ingest_listing_send_email(self):
        alert = self.__set_up_an_alert()
        kenny_u_pull_listing_data = {
            "make": "Toyota",
            "model": "Corolla",
            "year": "1996",
            "date_listed": "2020-01-01",
            "row_id": "A12",
            "branch": "Ottawa",
            "listing_url": "https://www.kennyupull.com/listing/A12",
            "client_id": str(alert.external_id),
        }

        ingest_listening(kenny_u_pull_listing_data=kenny_u_pull_listing_data)

        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            f"Hey! You have a new listing for a {alert.vehicle}!",
        )
        self.assertEqual(
            mail.outbox[0].body, f'You can go visit the listing on their website at {kenny_u_pull_listing_data["listing_url"]}'
        )
        self.assertEqual(mail.outbox[0].from_email, "support@kenny-u-watch.com")
        self.assertEqual(
            mail.outbox[0].to,
            [
                alert.user.email,
            ],
        )

    def test_ingest_listing_no_matching_alerts(self):
        alert = self.__set_up_an_alert()
        kenny_u_pull_listing_data = {
            "make": "Honda",
            "model": "Civic",
            "year": "1996",
            "date_listed": "2020-01-01",
            "row_id": "A12",
            "branch": "Ottawa",
            "listing_url": "https://www.kennyupull.com/listing/A12",
            "client_id": str(alert.external_id),
        }

        ingest_listening(kenny_u_pull_listing_data=kenny_u_pull_listing_data)

        self.assertEqual(len(mail.outbox), 0)

    def test_ingest_listing_matching_alerts_but_not_branch(self):
        alert = self.__set_up_an_alert(branch="St-Test")
        kenny_u_pull_listing_data = {
            "make": "Toyota",
            "model": "Corolla",
            "year": "1996",
            "date_listed": "2020-01-01",
            "row_id": "A12",
            "branch": "Ottawa",
            "listing_url": "https://www.kennyupull.com/listing/A12",
            "client_id": str(alert.external_id),
        }

        ingest_listening(kenny_u_pull_listing_data=kenny_u_pull_listing_data)

        self.assertEqual(len(mail.outbox), 0)

    def test_ingest_listing_no_alerts_in_the_database(self):
        Alert.objects.all().delete()  # Delete all alerts in the database and ensure there are none.
        kenny_u_pull_listing_data = {
            "make": "Honda",
            "model": "Civic",
            "year": "1996",
            "date_listed": "2020-01-01",
            "row_id": "A12",
            "branch": "Ottawa",
            "listing_url": "https://www.kennyupull.com/listing/A12",
            "client_id": "1234",
        }

        ingest_listening(kenny_u_pull_listing_data=kenny_u_pull_listing_data)

        self.assertEqual(len(mail.outbox), 0)
