from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from alerts.models import Alert, Vehicle
from alerts.serializers import AlertSerializer, CreateAlertSerializer
from alerts.constants import ALERT_NOT_UPDATED_MESSAGE, ALERT_DOES_NOT_EXIST_MESSAGE


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_alerts(request) -> JsonResponse:
    """
    Get all alerts for a user.
    """
    user = request.user.id
    alerts = Alert.objects.filter(user=user)
    serializer = AlertSerializer(alerts, many=True)

    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def get_alert(request, alert_id: int):
    """
    Get an alert for a user.
    """
    user = request.user.id

    try:
        alert = Alert.objects.get(user=user, id=alert_id)
        serializer = AlertSerializer(alert)

        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

    except Alert.DoesNotExist:
        return JsonResponse({"error": ALERT_DOES_NOT_EXIST_MESSAGE}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def create_alert(request):
    """
    Create an alert for a user.
    """
    user = request.user
    data = request.data
    create_serializer = CreateAlertSerializer(data=data)

    if not create_serializer.is_valid():
        return JsonResponse(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    valid_data = create_serializer.validated_data
    vehicle, _ = Vehicle.objects.get_or_create(
        manufacturer_name=valid_data["vehicle"]["manufacturer_name"],
        model_name=valid_data["vehicle"]["model_name"],
        model_year=valid_data["vehicle"]["model_year"],
    )

    alert = Alert.objects.create(user=user, vehicle=vehicle, branch=valid_data.get("branch"))
    alert_serializer = AlertSerializer(alert)

    return JsonResponse(alert_serializer.data, status=status.HTTP_201_CREATED)


@api_view(["PUT"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def update_alert(request, alert_id: int):
    """
    Update an alert for a user.
    """
    user = request.user.id
    data = request.data
    data["user"] = user

    try:
        alert = Alert.objects.get(user=user, id=alert_id)
        alert_fields_to_update = []
        vehicle_fields_to_update = []

        if new_manufacturer_name := data.get("vehicle", {}).get("manufacturer_name"):
            if new_manufacturer_name != alert.vehicle.manufacturer_name:
                alert.vehicle.manufacturer_name = new_manufacturer_name
                vehicle_fields_to_update.append("vehicle__manufacturer_name")

        if new_model_name := data.get("vehicle", {}).get("model_name"):
            if new_model_name != alert.vehicle.model_name:
                alert.vehicle.model_name = new_model_name
                vehicle_fields_to_update.append("vehicle__model_name")

        if new_model_year := data.get("vehicle", {}).get("model_year"):
            if new_model_year != alert.vehicle.model_year:
                alert.vehicle.model_year = new_model_year
                vehicle_fields_to_update.append("vehicle__model_year")

        new_branch = data.get("branch")
        if new_branch != alert.branch:
            alert.branch = new_branch
            alert_fields_to_update.append("branch")

        if not vehicle_fields_to_update and not alert_fields_to_update:
            return JsonResponse({"error": ALERT_NOT_UPDATED_MESSAGE}, status=status.HTTP_400_BAD_REQUEST)

        if vehicle_fields_to_update:
            alert.vehicle.save()

        if alert_fields_to_update:
            alert.save()

        serializer = AlertSerializer(alert)

        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    except Alert.DoesNotExist:
        return JsonResponse({"error": ALERT_DOES_NOT_EXIST_MESSAGE}, status=status.HTTP_404_NOT_FOUND)


@api_view(["DELETE"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def delete_alert(request, alert_id: int):
    """
    Delete an alert for a user.
    """
    user = request.user.id

    try:
        alert = Alert.objects.get(user=user, id=alert_id)
        alert.delete()
        return JsonResponse({}, status=status.HTTP_204_NO_CONTENT)

    except Alert.DoesNotExist:
        return JsonResponse({"error": ALERT_DOES_NOT_EXIST_MESSAGE}, status=status.HTTP_404_NOT_FOUND)
