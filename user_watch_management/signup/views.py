from rest_framework.decorators import api_view
from rest_framework import status
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from signup.serializers import CreateUserSerializer


@api_view(["POST"])
@csrf_exempt
def signup(request) -> JsonResponse:
    """
    Create a user.
    """
    data = request.data
    create_serializer = CreateUserSerializer(data=data)

    if not create_serializer.is_valid():
        return JsonResponse(create_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Create the user.
    create_serializer.save()

    return JsonResponse({}, status=status.HTTP_201_CREATED)
