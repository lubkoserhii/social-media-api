from django.contrib.auth import get_user_model
from django.test import TestCase

from user.models import Profile
from user.serializers import ProfileSerializer, UserRegisterSerializer


class UserRegisterSerializerTests(TestCase):
    def setUp(self):
        self.user_data = {
            "username": "petro",
            "email": "petro@example.com",
            "password": "test-password",
        }

    def test_create_user_does_not_create_profile(self):
        serializer = UserRegisterSerializer(data=self.user_data)

        self.assertTrue(serializer.is_valid(), serializer.errors)
        user = serializer.save()

        self.assertTrue(user.check_password(self.user_data["password"]))
        self.assertFalse(Profile.objects.filter(user=user).exists())


class ProfileSerializerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="alice",
            email="alice@example.com",
            password="test-password",
        )
        self.follower_user = get_user_model().objects.create_user(
            username="ivan",
            email="ivan@example.com",
            password="test-password",
        )
        self.followed_user = get_user_model().objects.create_user(
            username="charlie",
            email="charlie@example.com",
            password="test-password",
        )
        self.profile = Profile.objects.create(user=self.user, bio="Test bio")
        self.follower_profile = Profile.objects.create(user=self.follower_user)
        self.followed_profile = Profile.objects.create(user=self.followed_user)

    def test_serializes_user_data_and_follow_counts(self):
        self.follower_profile.following.add(self.profile)
        self.profile.following.add(self.followed_profile)

        data = ProfileSerializer(self.profile).data

        self.assertEqual(data["username"], self.user.username)
        self.assertEqual(data["email"], self.user.email)
        self.assertEqual(data["followers_count"], 1)
        self.assertEqual(data["following_count"], 1)
