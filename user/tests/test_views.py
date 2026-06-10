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


class LogoutTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="logout-user",
            email="logout@example.com",
            password="test-password",
        )
        Profile.objects.create(user=self.user)

    def test_logout_revokes_tokens_until_next_login(self):
        login_response = self.client.post(
            reverse("user:token_obtain_pair"),
            {
                "email": self.user.email,
                "password": "test-password",
            },
        )
        access = login_response.data["access"]
        refresh = login_response.data["refresh"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access}")

        logout_response = self.client.post(reverse("user:logout"))

        self.assertEqual(logout_response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            self.client.get(reverse("user:profile-list")).status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
        self.assertEqual(
            self.client.post(
                reverse("user:token_refresh"),
                {"refresh": refresh},
            ).status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

        self.client.credentials()
        new_login_response = self.client.post(
            reverse("user:token_obtain_pair"),
            {
                "email": self.user.email,
                "password": "test-password",
            },
        )
        self.assertEqual(new_login_response.status_code, status.HTTP_200_OK)

        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {new_login_response.data['access']}"
        )
        self.assertEqual(
            self.client.get(reverse("user:profile-list")).status_code,
            status.HTTP_200_OK,
        )
