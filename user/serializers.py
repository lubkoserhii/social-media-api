from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

from user.models import Profile


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["token_version"] = user.token_version
        return token


class LogoutSerializer(serializers.Serializer):
    @transaction.atomic
    def save(self, **kwargs):
        user = (
            get_user_model()
            .objects.select_for_update()
            .get(pk=self.context["request"].user.pk)
        )

        for token in OutstandingToken.objects.filter(user=user):
            BlacklistedToken.objects.get_or_create(token=token)

        user.token_version += 1
        user.save(update_fields=["token_version"])


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=5)

    class Meta:
        model = get_user_model()
        fields = ("id", "email", "username", "password")

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)


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

    def validate(self, attrs):
        request = self.context.get("request")
        if (
            self.instance is None
            and request
            and Profile.objects.filter(user=request.user).exists()
        ):
            raise serializers.ValidationError("You already have a profile.")
        return attrs
