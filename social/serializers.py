from rest_framework import serializers
from social.models import Post, Comment


class CommentSerializer(serializers.ModelSerializer):
    author_email = serializers.CharField(source="author.email", read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "post", "author", "author_email", "text", "created_at")
        read_only_fields = ("author",)


class PostSerializer(serializers.ModelSerializer):
    author_email = serializers.CharField(source="author.email", read_only=True)
    likes_count = serializers.IntegerField(source="likes.count", read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = (
            "id",
            "author",
            "author_email",
            "text",
            "image",
            "hashtags",
            "created_at",
            "likes_count",
            "comments",
        )
        read_only_fields = ("author",)
