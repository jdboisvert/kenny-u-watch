from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


from alerts.models import Alert
from alerts.serializers import AlertSerializer


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
        serializer = AlertSerializer(alert=alert)
            
        return JsonResponse({serializer.data}, safe=False, status=status.HTTP_200_OK)
    except Alert.DoesNotExist:
        return JsonResponse({"error": "Alert does not exist"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
@csrf_exempt
@permission_classes([IsAuthenticated])
def create_alert(request):
    """
    Create an alert for a user. 
    """
    user = request.user.id
    data = request.data
    data["user"] = user
    serializer = AlertSerializer(data=data)
    
    if serializer.is_valid():
        serializer.save()
        return JsonResponse({"success": "Alert created successfully"}, status=status.HTTP_201_CREATED)
    else:
        return JsonResponse({"error": "Alert not created"}, status=status.HTTP_400_BAD_REQUEST)
    
    
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
        serializer = AlertSerializer(alert=alert, data=data)
        
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({"success": "Alert updated successfully"}, status=status.HTTP_200_OK)
        else:
            return JsonResponse({"error": "Alert not updated"}, status=status.HTTP_400_BAD_REQUEST)
    except Alert.DoesNotExist:
        return JsonResponse({"error": "Alert does not exist"}, status=status.HTTP_404_NOT_FOUND)
    

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
        return JsonResponse({"success": "Alert deleted successfully"}, status=status.HTTP_200_OK)
    except Alert.DoesNotExist:
        return JsonResponse({"error": "Alert does not exist"}, status=status.HTTP_404_NOT_FOUND)