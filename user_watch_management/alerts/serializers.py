from rest_framework import serializers
from alerts.models import Alert
from alerts.models import Vehicle


class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ["manufacturer_name", "model_name", "model_year"]


class AlertSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer()

    class Meta:
        model = Alert
        fields = ["id", "vehicle", "branch", "created", "modified"]
        extra_kwargs = {"branch": {"required": False}}


class CreateAlertSerializer(serializers.ModelSerializer):
    vehicle = VehicleSerializer()

    class Meta:
        model = Alert
        fields = ["branch", "vehicle"]
        extra_kwargs = {"branch": {"required": False}}
