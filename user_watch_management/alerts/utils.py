from typing import Optional

from alerts.models import Alert, Vehicle
from django.db import transaction
from django.conf import settings
from django.contrib.auth.models import User

import requests

from alerts.exceptions import SubscriptionFailureException


def handle_create_alert(manufacturer_name: str, model_name: str, model_year: int, user: User, branch: Optional[str] = None) -> Alert:
    """
    Handle creating the alert for the user and subscribing to the alert. This will not save to the database if
    we are unable to get a response from the alert producer.

    :param manufacturer_name: The manufacturer name of the vehicle (ex: "Toyota")
    :param model_name: The model name of the vehicle (ex: "Corolla")
    :param model_year: The model year of the vehicle (ex: 2021)
    :param user: The user that is creating the alert.
    :param branch: The branch of the vehicle (ex: "Ottawa")
    :return: The alert that was created.
    :raises SubscriptionFailureException: Raised if we are unable to subscribe to the alert.
    """
    with transaction.atomic():
        vehicle = Vehicle.objects.create(
            manufacturer_name=manufacturer_name,
            model_name=model_name,
            model_year=model_year,
        )

        alert = Alert.objects.create(user=user, vehicle=vehicle, branch=branch)

        response = requests.post(
            settings.ALERT_PRODUCER_URL,
            json={
                "model": vehicle.model_name,
                "manufacturer": vehicle.manufacturer_name,
                "year": vehicle.model_year,
                "client_id": str(alert.external_id),
            }
        )
        if not response.ok:
            # Break the transaction and delete the alert if we are unable to subscribe to the alert.
            raise SubscriptionFailureException("Failed to subscribe to alert.")

        return alert
