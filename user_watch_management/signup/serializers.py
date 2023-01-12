from rest_framework import serializers
from django.contrib.auth.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a user.
    """

    class Meta:
        model = User
        fields = ["email", "username", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        """
        Create a user with the given username and password.
        """
        user = User.objects.create_user(
            username=validated_data["username"], password=validated_data["password"], email=validated_data["username"]
        )
        return user
