from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from social.models import Comment, Post
from user.models import Profile


class SocialViewsTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="alice",
            email="alice@example.com",
            password="test-password",
        )
        self.followed_user = get_user_model().objects.create_user(
            username="bob",
            email="bob@example.com",
            password="test-password",
        )
        self.other_user = get_user_model().objects.create_user(
            username="charlie",
            email="charlie@example.com",
            password="test-password",
        )
        self.profile = Profile.objects.create(user=self.user)
        self.followed_profile = Profile.objects.create(user=self.followed_user)
        Profile.objects.create(user=self.other_user)
        self.profile.following.add(self.followed_profile)
        self.client.force_authenticate(self.user)

    def test_post_list_contains_own_and_followed_users_posts(self):
        own_post = Post.objects.create(author=self.user, text="Own post")
        followed_post = Post.objects.create(
            author=self.followed_user,
            text="Followed post",
        )
        Post.objects.create(author=self.other_user, text="Other post")

        response = self.client.get(reverse("social:post-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [post["id"] for post in response.data],
            [followed_post.id, own_post.id],
        )

    def test_create_post_assigns_authenticated_user_as_author(self):
        response = self.client.post(
            reverse("social:post-list"),
            {"text": "New post"},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post = Post.objects.get(pk=response.data["id"])
        self.assertEqual(post.author, self.user)

    def test_create_comment_assigns_authenticated_user_as_author(self):
        post = Post.objects.create(
            author=self.followed_user,
            text="Post with a comment",
        )

        response = self.client.post(
            reverse("social:comment-list"),
            {"post": post.pk, "text": "My comment"},
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        comment = Comment.objects.get(pk=response.data["id"])
        self.assertEqual(comment.author, self.user)

    def test_like_followed_users_post(self):
        post = Post.objects.create(
            author=self.followed_user,
            text="Post to like",
        )

        response = self.client.post(reverse("social:post-like", kwargs={"pk": post.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"detail": "Post liked."})
        self.assertIn(self.user, post.likes.all())

    def test_like_action_removes_existing_like(self):
        post = Post.objects.create(
            author=self.followed_user,
            text="Liked post",
        )
        post.likes.add(self.user)

        response = self.client.post(reverse("social:post-like", kwargs={"pk": post.pk}))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"detail": "Post unliked."})
        self.assertNotIn(self.user, post.likes.all())


class SocialViewsWithoutProfileTests(APITestCase):
    def test_post_list_returns_own_posts_without_profile(self):
        user = get_user_model().objects.create_user(
            username="without-profile",
            email="without-profile@example.com",
            password="test-password",
        )
        own_post = Post.objects.create(author=user, text="Own post")
        self.client.force_authenticate(user)

        response = self.client.get(reverse("social:post-list"))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([post["id"] for post in response.data], [own_post.id])
