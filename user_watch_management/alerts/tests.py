import json
from typing import Optional
from uuid import uuid4
from django.test import TestCase

from alerts.models import Vehicle, Alert
from django.contrib.auth.models import User

from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

def create_alert_as_dict(alert: Alert) -> dict:
    return  {
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
        user =  User.objects.create_user(username_and_email, username_and_email, str(uuid4()))
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
    test_url = '/api/v1/get-alerts'
    
    def setUp(self) -> None:
        self.maxDiff = None
        username_and_email = "tester@test.com" 
        self.client = APIClient()
        self.user = User.objects.create_user(username_and_email, username_and_email, password=str(uuid4()))
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
                
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
        expected_content = [
            create_alert_as_dict(alert1),
            create_alert_as_dict(alert2)
        ]
        self.assertCountEqual(content, expected_content)
        
    def test_get_alerts_with_multiple_alerts_and_branch(self):
        branch = "Test Branch"
        alert1 = self.__set_up_an_alert(branch=branch)
        alert2 = self.__set_up_an_alert(branch=branch)
        
        response = self.client.get(self.test_url)
        
        self.assertEqual(response.status_code, 200)
        
        content = json.loads(response.content)
        expected_content = [
            create_alert_as_dict(alert1),
            create_alert_as_dict(alert2)
        ]
        self.assertCountEqual(content, expected_content)
        
    def test_get_alerts_with_multiple_alerts_and_different_branches(self):
        branch1 = "Test Branch"
        branch2 = "Test Branch 2"
        alert1 = self.__set_up_an_alert(branch=branch1)
        alert2 = self.__set_up_an_alert(branch=branch2)
        
        response = self.client.get(self.test_url)
                
        self.assertEqual(response.status_code, 200)
        
        content = json.loads(response.content)
        expected_content = [
            create_alert_as_dict(alert1),
            create_alert_as_dict(alert2)
        ]
        self.assertCountEqual(content, expected_content)
        
    def test_get_alerts_with_multiple_alerts_and_different_users(self):
        username_and_email2 = "tester2@test.com"
        user2 =  User.objects.create_user(username_and_email2, username_and_email2, str(uuid4()))
        
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

