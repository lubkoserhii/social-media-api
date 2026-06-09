from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=5)

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "username", "password")

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
