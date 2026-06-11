from django.contrib.auth import get_user_model
from django.test import TestCase

from social.models import Comment, Post
from social.serializers import CommentSerializer, PostSerializer


class SocialSerializersTests(TestCase):
    def setUp(self) -> None:
        self.author = get_user_model().objects.create_user(
            username="alice",
            email="alice@example.com",
            password="test-password",
        )
        self.other_user = get_user_model().objects.create_user(
            username="bob",
            email="bob@example.com",
            password="test-password",
        )
        self.post = Post.objects.create(
            author=self.author,
            text="My first post",
        )
        self.comment = Comment.objects.create(
            post=self.post,
            author=self.other_user,
            text="Welcome!",
        )
        self.post.likes.add(self.other_user)

    def test_comment_serializer_includes_author_email(self) -> None:
        data = CommentSerializer(self.comment).data

        self.assertEqual(data["author_email"], self.other_user.email)

    def test_post_serializer_includes_custom_related_data(self) -> None:
        data = PostSerializer(self.post).data

        self.assertEqual(data["author_email"], self.author.email)
        self.assertEqual(data["likes_count"], 1)
        self.assertEqual(len(data["comments"]), 1)
        self.assertEqual(data["comments"][0]["id"], self.comment.id)
        self.assertEqual(
            data["comments"][0]["author_email"],
            self.other_user.email,
        )
