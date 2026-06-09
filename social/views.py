from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import SearchFilter
from social.models import Post
from social.serializers import PostSerializer
from utils.permissions import IsOwnerOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly,
    ]
    filter_backends = [SearchFilter]
    search_fields = ["content", "hashtags"]

    def get_queryset(self):
        user = self.request.user
        following_profiles = user.profile.following.all()
        following_users = [profile.user for profile in following_profiles]

        return (
            Post.objects.filter(Q(author=user) | Q(author__in=following_users))
            .distinct()
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=["POST"])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            return Response({"detail": "Post unliked."}, status=status.HTTP_200_OK)
        else:
            post.likes.add(user)
            return Response({"detail": "Post liked."}, status=status.HTTP_200_OK)
