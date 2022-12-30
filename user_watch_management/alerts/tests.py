from typing import Optional
from uuid import uuid4
from django.test import TestCase

from alerts.models import Vehicle, Alert
from django.contrib.auth.models import User

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