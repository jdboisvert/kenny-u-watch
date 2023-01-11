import json
from typing import Optional
from unittest import mock
from uuid import uuid4
from django.test import TestCase

from alerts.models import Vehicle, Alert
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from alerts.constants import ALERT_NOT_UPDATED_MESSAGE


def create_alert_as_dict(alert: Alert) -> dict:
    return {
        "id": alert.id,
        "vehicle": {
            "model_year": alert.vehicle.model_year,
            "manufacturer_name": alert.vehicle.manufacturer_name,
            "model_name": alert.vehicle.model_name,
        },
        "branch": alert.branch,
        "created": alert.created.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        "modified": alert.modified.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
    }


class AlertTests(TestCase):
    def __set_up_an_alert(self, branch: Optional[str] = None) -> Alert:
        manufacturer_name = "Toyota"
        model_name = "Corolla"
        model_year = "1996"

        vehicle = Vehicle.objects.create(manufacturer_name=manufacturer_name, model_year=model_year, model_name=model_name)

        username_and_email = "john_doe@testing.com"
        user = User.objects.create_user(username_and_email, username_and_email, str(uuid4()))
        return Alert.objects.create(user=user, vehicle=vehicle, branch=branch)

    def test_str_correct_value_with_no_branch(self):
        alert = self.__set_up_an_alert()

        self.assertEqual(str(alert), f"{alert.user.username}'s alert on a {alert.vehicle}")

    def test_str_correct_value_with_a_branch(self):
        branch = "Test Branch"
        alert = self.__set_up_an_alert(branch=branch)

        self.assertEqual(str(alert), f"{alert.user.username}'s alert on a {alert.vehicle} at {alert.branch}")


class VehicleTests(TestCase):
    def test_str_correct_value(self):
        manufacturer_name = "Toyota"
        model_name = "Corolla"
        model_year = "1996"

        vehicle = Vehicle(manufacturer_name=manufacturer_name, model_year=model_year, model_name=model_name)

        self.assertEqual(str(vehicle), f"{vehicle.model_year} {vehicle.manufacturer_name} {vehicle.model_name}")


class GetAlertsTests(TestCase):
    test_url = "/alerts/v1/get-alerts"

    def setUp(self) -> None:
        self.maxDiff = None
        username_and_email = "tester@test.com"
        self.client = APIClient()
        self.user = User.objects.create_user(username_and_email, username_and_email, password=str(uuid4()))
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        return super().setUp()

    def __set_up_an_alert(self, user: Optional[User] = None, branch: Optional[str] = None) -> Alert:
        manufacturer_name = "Toyota"
        model_name = "Corolla"
        model_year = "1996"

        vehicle = Vehicle.objects.create(manufacturer_name=manufacturer_name, model_year=model_year, model_name=model_name)
        user = user if user else self.user

        return Alert.objects.create(user=user, vehicle=vehicle, branch=branch)

    def test_get_alerts_with_a_single_alert(self):
        alert = self.__set_up_an_alert()

        response = self.client.get(self.test_url)

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        expected_content = [
            create_alert_as_dict(alert),
        ]
        self.assertCountEqual(content, expected_content)

    def test_get_alerts_with_no_alerts(self):
        response = self.client.get(self.test_url)

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        self.assertCountEqual(content, [])

    def test_get_alerts_with_multiple_alerts(self):
        alert1 = self.__set_up_an_alert()
        alert2 = self.__set_up_an_alert()

        response = self.client.get(self.test_url)

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        expected_content = [create_alert_as_dict(alert1), create_alert_as_dict(alert2)]
        self.assertCountEqual(content, expected_content)

    def test_get_alerts_with_multiple_alerts_and_branch(self):
        branch = "Test Branch"
        alert1 = self.__set_up_an_alert(branch=branch)
        alert2 = self.__set_up_an_alert(branch=branch)

        response = self.client.get(self.test_url)

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        expected_content = [create_alert_as_dict(alert1), create_alert_as_dict(alert2)]
        self.assertCountEqual(content, expected_content)

    def test_get_alerts_with_multiple_alerts_and_different_branches(self):
        branch1 = "Test Branch"
        branch2 = "Test Branch 2"
        alert1 = self.__set_up_an_alert(branch=branch1)
        alert2 = self.__set_up_an_alert(branch=branch2)

        response = self.client.get(self.test_url)

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        expected_content = [create_alert_as_dict(alert1), create_alert_as_dict(alert2)]
        self.assertCountEqual(content, expected_content)

    def test_get_alerts_with_multiple_alerts_and_different_users(self):
        username_and_email2 = "tester2@test.com"
        user2 = User.objects.create_user(username_and_email2, username_and_email2, str(uuid4()))

        alert1 = self.__set_up_an_alert(user=self.user)
        self.__set_up_an_alert(user=user2)

        response = self.client.get(self.test_url)

        self.assertEqual(response.status_code, 200)

        # Should only contain the alerts that belong to the logged in user not the other user.
        expected_content = [
            create_alert_as_dict(alert1),
        ]
        content = json.loads(response.content)
        self.assertEqual(content, expected_content)


class CreateAlertsTests(TestCase):
    test_url = "/alerts/v1/create-alert"

    def setUp(self) -> None:
        self.maxDiff = None
        username_and_email = "tester@test.com"
        self.client = APIClient()
        self.user = User.objects.create_user(username_and_email, username_and_email, password=str(uuid4()))
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        return super().setUp()

    def test_create_alert_with_valid_data(self):
        manufacturer_name = "Toyota"
        model_name = "Corolla"
        model_year = "1996"
        branch = "Test Branch"

        data = {
            "vehicle": {
                "manufacturer_name": manufacturer_name,
                "model_name": model_name,
                "model_year": model_year,
            },
            "branch": branch,
        }

        response = self.client.post(self.test_url, data=data, format="json")

        self.assertEqual(response.status_code, 201)

        content = json.loads(response.content)
        expected_content = {
            "id": mock.ANY,
            "vehicle": {
                "model_year": model_year,
                "manufacturer_name": manufacturer_name,
                "model_name": model_name,
            },
            "branch": branch,
            "created": mock.ANY,
            "modified": mock.ANY,
        }
        self.assertCountEqual(content, expected_content)

    def test_create_alert_with_valid_data_without_branch(self):
        manufacturer_name = "Toyota"
        model_name = "Corolla"
        model_year = "1996"

        data = {
            "vehicle": {
                "manufacturer_name": manufacturer_name,
                "model_name": model_name,
                "model_year": model_year,
            }
        }
        response = self.client.post(self.test_url, data=data, format="json")

        self.assertEqual(response.status_code, 201)

        content = json.loads(response.content)
        expected_content = {
            "id": mock.ANY,
            "vehicle": {
                "model_year": model_year,
                "manufacturer_name": manufacturer_name,
                "model_name": model_name,
            },
            "branch": None,
            "created": mock.ANY,
            "modified": mock.ANY,
        }
        self.assertCountEqual(content, expected_content)

    def test_create_alert_with_invalid_data_missing_model_year(self):
        data = {
            "vehicle": {
                "manufacturer_name": "Toyota",
                "model_name": "Corolla",
            }
        }

        response = self.client.post(self.test_url, data=data, format="json")

        self.assertEqual(response.status_code, 400)

        content = json.loads(response.content)
        expected_content = {
            "vehicle": {"model_year": ["This field is required."]},
        }
        self.assertDictEqual(content, expected_content)

    def test_create_alert_with_invalid_data_missing_model_name(self):
        data = {
            "vehicle": {
                "manufacturer_name": "Toyota",
                "model_year": "1996",
            }
        }

        response = self.client.post(self.test_url, data=data, format="json")

        self.assertEqual(response.status_code, 400)

        content = json.loads(response.content)
        expected_content = {
            "vehicle": {"model_name": ["This field is required."]},
        }
        self.assertDictEqual(content, expected_content)

    def test_create_alert_with_invalid_data_missing_manufacturer_name(self):
        data = {
            "vehicle": {
                "model_name": "Corolla",
                "model_year": "1996",
            }
        }

        response = self.client.post(self.test_url, data=data, format="json")

        self.assertEqual(response.status_code, 400)

        content = json.loads(response.content)
        expected_content = {
            "vehicle": {
                "manufacturer_name": ["This field is required."],
            },
        }
        self.assertDictEqual(content, expected_content)


class UpdateAlertsTests(TestCase):
    test_url = "/alerts/v1/update-alert"

    def setUp(self) -> None:
        self.maxDiff = None
        username_and_email = "tester@test.com"
        self.client = APIClient()
        self.user = User.objects.create_user(username_and_email, username_and_email, password=str(uuid4()))
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        return super().setUp()

    def __set_up_an_alert(self, user: Optional[User] = None, branch: Optional[str] = None) -> Alert:
        manufacturer_name = "Toyota"
        model_name = "Corolla"
        model_year = "1996"

        vehicle = Vehicle.objects.create(manufacturer_name=manufacturer_name, model_year=model_year, model_name=model_name)
        user = user if user else self.user

        return Alert.objects.create(user=user, vehicle=vehicle, branch=branch)

    def test_update_alert_with_valid_data(self):
        manufacturer_name = "Honda"
        model_name = "Civic"
        model_year = "2001"
        branch = "Test Branch"

        alert = self.__set_up_an_alert()

        data = {
            "vehicle": {
                "manufacturer_name": manufacturer_name,
                "model_name": model_name,
                "model_year": model_year,
            },
            "branch": branch,
        }

        url = f"{self.test_url}/{alert.id}"
        response = self.client.put(url, data=data, format="json")

        self.assertEqual(response.status_code, 200)

        # Ensure that the response contains the expected data
        content = json.loads(response.content)
        expected_content = {
            "id": alert.id,
            "vehicle": {
                "model_year": model_year,
                "manufacturer_name": manufacturer_name,
                "model_name": model_name,
            },
            "branch": branch,
            "created": mock.ANY,
            "modified": mock.ANY,
        }
        self.assertCountEqual(content, expected_content)

        # Ensure that the alert was updated in the database
        alert.refresh_from_db()
        alert.vehicle.refresh_from_db()
        self.assertEqual(alert.branch, branch)
        self.assertEqual(alert.vehicle.manufacturer_name, manufacturer_name)
        self.assertEqual(alert.vehicle.model_name, model_name)
        self.assertEqual(alert.vehicle.model_year, model_year)

    def test_update_alert_with_valid_data_without_branch(self):
        manufacturer_name = "Honda"
        model_name = "Civic"
        model_year = "2001"

        alert = self.__set_up_an_alert(branch="Test Branch")

        data = {
            "vehicle": {
                "manufacturer_name": manufacturer_name,
                "model_name": model_name,
                "model_year": model_year,
            },
        }

        url = f"{self.test_url}/{alert.id}"
        response = self.client.put(url, data=data, format="json")

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        expected_content = {
            "id": alert.id,
            "vehicle": {
                "model_year": model_year,
                "manufacturer_name": manufacturer_name,
                "model_name": model_name,
            },
            "branch": None,
            "created": mock.ANY,
            "modified": mock.ANY,
        }
        self.assertCountEqual(content, expected_content)

        # Ensure that the alert was updated in the database
        alert.refresh_from_db()
        alert.vehicle.refresh_from_db()
        self.assertIsNone(alert.branch)
        self.assertEqual(alert.vehicle.manufacturer_name, manufacturer_name)
        self.assertEqual(alert.vehicle.model_name, model_name)
        self.assertEqual(alert.vehicle.model_year, model_year)

    def test_update_alert_with_data_missing_model_year(self):
        manufacturer_name = "Honda"
        model_name = "Civic"

        alert = self.__set_up_an_alert()
        current_model_year = alert.vehicle.model_year

        data = {
            "vehicle": {
                "manufacturer_name": manufacturer_name,
                "model_name": model_name,
            }
        }

        url = f"{self.test_url}/{alert.id}"
        response = self.client.put(url, data=data, format="json")

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        expected_content = {
            "id": alert.id,
            "vehicle": {
                "model_year": current_model_year,
                "manufacturer_name": manufacturer_name,
                "model_name": model_name,
            },
            "branch": None,
            "created": mock.ANY,
            "modified": mock.ANY,
        }
        self.assertDictEqual(content, expected_content)

        # Ensure that the alert was updated in the database
        alert.refresh_from_db()
        alert.vehicle.refresh_from_db()
        self.assertIsNone(alert.branch)
        self.assertEqual(alert.vehicle.manufacturer_name, manufacturer_name)
        self.assertEqual(alert.vehicle.model_name, model_name)
        self.assertEqual(alert.vehicle.model_year, current_model_year)

    def test_update_alert_with_data_missing_model_name(self):
        manufacturer_name = "Honda"
        model_year = "2001"

        alert = self.__set_up_an_alert()
        current_model_name = alert.vehicle.model_name

        data = {
            "vehicle": {
                "manufacturer_name": manufacturer_name,
                "model_year": model_year,
            }
        }

        url = f"{self.test_url}/{alert.id}"
        response = self.client.put(url, data=data, format="json")

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        expected_content = {
            "id": alert.id,
            "vehicle": {
                "model_year": model_year,
                "manufacturer_name": manufacturer_name,
                "model_name": current_model_name,
            },
            "branch": None,
            "created": mock.ANY,
            "modified": mock.ANY,
        }
        self.assertDictEqual(content, expected_content)

        # Ensure that the alert was updated in the database
        alert.refresh_from_db()
        alert.vehicle.refresh_from_db()
        self.assertIsNone(alert.branch)
        self.assertEqual(alert.vehicle.manufacturer_name, manufacturer_name)
        self.assertEqual(alert.vehicle.model_name, current_model_name)
        self.assertEqual(alert.vehicle.model_year, model_year)

    def test_update_alert_with_data_missing_manufacturer_name(self):
        model_name = "Civic"
        model_year = "2001"

        alert = self.__set_up_an_alert()
        current_manufacturer_name = alert.vehicle.manufacturer_name

        data = {
            "vehicle": {
                "model_name": model_name,
                "model_year": model_year,
            }
        }

        url = f"{self.test_url}/{alert.id}"
        response = self.client.put(url, data=data, format="json")

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        expected_content = {
            "id": alert.id,
            "vehicle": {
                "model_year": model_year,
                "manufacturer_name": current_manufacturer_name,
                "model_name": model_name,
            },
            "branch": None,
            "created": mock.ANY,
            "modified": mock.ANY,
        }
        self.assertDictEqual(content, expected_content)

        # Ensure that the alert was updated in the database
        alert.refresh_from_db()
        alert.vehicle.refresh_from_db()
        self.assertIsNone(alert.branch)
        self.assertEqual(alert.vehicle.manufacturer_name, current_manufacturer_name)
        self.assertEqual(alert.vehicle.model_name, model_name)
        self.assertEqual(alert.vehicle.model_year, model_year)

    def test_update_alert_with_data_missing_vehicle(self):
        alert = self.__set_up_an_alert()
        branch = "New branch"

        data = {
            "branch": branch,
        }

        previous_model_year = alert.vehicle.model_year
        previous_manufacturer_name = alert.vehicle.manufacturer_name
        previous_model_name = alert.vehicle.model_name

        url = f"{self.test_url}/{alert.id}"
        response = self.client.put(url, data=data, format="json")

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        expected_content = {
            "id": alert.id,
            "vehicle": {
                # Should be unchanged
                "model_year": alert.vehicle.model_year,
                "manufacturer_name": alert.vehicle.manufacturer_name,
                "model_name": alert.vehicle.model_name,
            },
            "branch": branch,
            "created": mock.ANY,
            "modified": mock.ANY,
        }
        self.assertDictEqual(content, expected_content)

        # Ensure that the alert was updated in the database
        alert.refresh_from_db()
        alert.vehicle.refresh_from_db()
        self.assertEqual(alert.branch, branch)
        self.assertEqual(alert.vehicle.model_year, previous_model_year)
        self.assertEqual(alert.vehicle.manufacturer_name, previous_manufacturer_name)
        self.assertEqual(alert.vehicle.model_name, previous_model_name)

    def test_update_alert_invalid_id(self):
        branch = "New branch"

        data = {
            "branch": branch,
        }

        url = f"{self.test_url}/-1"
        response = self.client.put(url, data=data, format="json")

        self.assertEqual(response.status_code, 404)

    def test_update_alert_invalid_non_existent_id(self):
        branch = "New branch"

        data = {
            "branch": branch,
        }

        url = f"{self.test_url}/12345678"
        response = self.client.put(url, data=data, format="json")

        self.assertEqual(response.status_code, 404)

    def test_update_alert_invalid_no_fields_updated(self):
        alert = self.__set_up_an_alert()

        data = {
            # The alert should not be updated if no new fields are provided
            "vehicle": {
                "manufacturer_name": alert.vehicle.manufacturer_name,
                "model_name": alert.vehicle.model_name,
                "model_year": alert.vehicle.model_year,
            },
            "branch": alert.branch,
        }

        url = f"{self.test_url}/{alert.id}"
        response = self.client.put(url, data=data, format="json")

        self.assertEqual(response.status_code, 400)

        content = json.loads(response.content)
        expected_content = {"error": ALERT_NOT_UPDATED_MESSAGE}
        self.assertDictEqual(content, expected_content)


class DeleteAlertTestCase(TestCase):
    test_url = "/alerts/v1/delete-alert"

    def setUp(self) -> None:
        self.maxDiff = None
        username_and_email = "tester@test.com"
        self.client = APIClient()
        self.user = User.objects.create_user(username_and_email, username_and_email, password=str(uuid4()))
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        return super().setUp()

    def __set_up_an_alert(self) -> Alert:
        vehicle = Vehicle.objects.create(
            manufacturer_name="Honda",
            model_name="Civic",
            model_year="2001",
        )
        alert = Alert.objects.create(
            vehicle=vehicle,
            branch="Test branch",
            user=self.user,
        )
        return alert

    def test_delete_alert(self):
        alert = self.__set_up_an_alert()

        url = f"{self.test_url}/{alert.id}"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204)

        # Ensure that the alert was deleted from the database
        with self.assertRaises(Alert.DoesNotExist):
            alert.refresh_from_db()

    def test_delete_alert_with_invalid_id(self):
        alert = self.__set_up_an_alert()

        url = f"{self.test_url}/-1"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)

        # Ensure that the alert was not deleted from the database
        alert.refresh_from_db()

    def test_delete_alert_with_non_existent_id(self):
        alert = self.__set_up_an_alert()

        url = f"{self.test_url}/100000"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 404)

        # Ensure that the alert was not deleted from the database
        alert.refresh_from_db()


class GetAlertTestCase(TestCase):
    test_url = "/alerts/v1/get-alert"

    def setUp(self) -> None:
        self.maxDiff = None
        username_and_email = "tester@test.com"
        self.client = APIClient()
        self.user = User.objects.create_user(username_and_email, username_and_email, password=str(uuid4()))
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        return super().setUp()

    def __set_up_an_alert(self) -> Alert:
        vehicle = Vehicle.objects.create(
            manufacturer_name="Honda",
            model_name="Civic",
            model_year="2001",
        )
        alert = Alert.objects.create(
            vehicle=vehicle,
            branch="Test branch",
            user=self.user,
        )
        return alert

    def test_get_alert(self):
        alert = self.__set_up_an_alert()

        url = f"{self.test_url}/{alert.id}"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        expected_content = create_alert_as_dict(alert=alert)
        self.assertDictEqual(content, expected_content)

    def test_get_alert_with_invalid_id(self):
        self.__set_up_an_alert()

        url = f"{self.test_url}/-1"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)

    def test_get_alert_with_non_existent_id(self):
        self.__set_up_an_alert()

        url = f"{self.test_url}/100000"
        response = self.client.get(url)

        self.assertEqual(response.status_code, 404)
