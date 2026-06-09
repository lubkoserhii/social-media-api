from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from user.models import Profile


class ProfileFollowActionsTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="alice",
            email="alice@example.com",
            password="test-password",
        )
        self.other_user = get_user_model().objects.create_user(
            username="george",
            email="george@example.com",
            password="test-password",
        )
        self.profile = Profile.objects.create(user=self.user)
        self.other_profile = Profile.objects.create(user=self.other_user)
        self.client.force_authenticate(self.user)

    def test_follow_profile(self):
        response = self.client.post(
            reverse(
                "user:profile-follow",
                kwargs={"pk": self.other_profile.pk},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {"detail": f"Successfully followed {self.other_user.username}."},
        )
        self.assertIn(self.other_profile, self.profile.following.all())

    def test_cannot_follow_own_profile(self):
        response = self.client.post(
            reverse(
                "user:profile-follow",
                kwargs={"pk": self.profile.pk},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {"detail": "You cannot follow yourself."},
        )
        self.assertNotIn(self.profile, self.profile.following.all())

    def test_unfollow_profile(self):
        self.profile.following.add(self.other_profile)

        response = self.client.post(
            reverse(
                "user:profile-unfollow",
                kwargs={"pk": self.other_profile.pk},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {"detail": f"Successfully unfollowed {self.other_user.username}."},
        )
        self.assertNotIn(self.other_profile, self.profile.following.all())

    def test_cannot_unfollow_profile_that_is_not_followed(self):
        response = self.client.post(
            reverse(
                "user:profile-unfollow",
                kwargs={"pk": self.other_profile.pk},
            )
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data,
            {"detail": "You are not following this user."},
        )
