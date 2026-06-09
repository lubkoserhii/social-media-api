from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase

from user.models import Profile


class UserModelsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="alice",
            email="alice@example.com",
            password="test-password",
        )
        self.other_user = get_user_model().objects.create_user(
            username="bob",
            email="bob@example.com",
            password="test-password",
        )
        self.profile = Profile.objects.create(user=self.user)
        self.other_profile = Profile.objects.create(user=self.other_user)

    def test_email_is_used_as_username_field(self):
        self.assertEqual(get_user_model().USERNAME_FIELD, "email")

    def test_email_must_be_unique(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            get_user_model().objects.create_user(
                username="another-alice",
                email=self.user.email,
                password="test-password",
            )

    def test_profile_can_follow_another_profile(self):
        self.profile.following.add(self.other_profile)

        self.assertIn(self.other_profile, self.profile.following.all())
        self.assertIn(self.profile, self.other_profile.followers.all())
