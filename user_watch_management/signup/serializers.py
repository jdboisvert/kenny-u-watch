from rest_framework import serializers
from django.contrib.auth.models import User


class CreateUserSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a user.
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "password")

    def create(self, validated_data):
        """
        Create a user with the given username and password.
        """
        user = User.objects.create_user(
            username=validated_data["username"], password=validated_data["password"], email=validated_data["username"]
        )
        return user
