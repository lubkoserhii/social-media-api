from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from user.models import Profile


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=5)

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "username", "password")

    def create(self, validated_data):
        with transaction.atomic():
            user = get_user_model().objects.create_user(**validated_data)
            Profile.objects.create(user=user)
            return user


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    followers_count = serializers.IntegerField(source="followers.count", read_only=True)
    following_count = serializers.IntegerField(source="following.count", read_only=True)

    class Meta:
        model = Profile
        fields = (
            "id",
            "username",
            "email",
            "bio",
            "profile_picture",
            "followers_count",
            "following_count",
        )
