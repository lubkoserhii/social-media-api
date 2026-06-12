from django.contrib.auth import get_user_model
from django.test import TestCase

from social.models import Comment, Post


class SocialModelsTests(TestCase):
    def setUp(self) -> None:
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

    def test_post_likes_and_comments(self) -> None:
        post = Post.objects.create(author=self.user, text="My first post")
        post.likes.add(self.other_user)
        comment = Comment.objects.create(
            post=post,
            author=self.other_user,
            text="Welcome!",
        )

        self.assertIn(post, self.other_user.liked_posts.all())
        self.assertIn(comment, post.comments.all())
