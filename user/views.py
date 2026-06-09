from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from user.serializers import UserRegisterSerializer, ProfileSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from user.models import Profile
from utils.permissions import IsOwnerOrReadOnly


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = get_user_model().objects.all()
    permission_classes = (AllowAny,)


class ProfileViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["user__username", "bio"]

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def follow(self, request, pk=None):
        profile_to_follow = self.get_object()
        current_profile = request.user.profile

        if current_profile == profile_to_follow:
            return Response(
                {"detail": "You cannot follow yourself."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        current_profile.following.add(profile_to_follow)
        return Response(
            {"detail": f"Successfully followed {profile_to_follow.user.username}."},
            status=status.HTTP_200_OK,
        )

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk=None):
        profile_to_unfollow = self.get_object()
        current_profile = request.user.profile

        if profile_to_unfollow in current_profile.following.all():
            current_profile.following.remove(profile_to_unfollow)
            return Response(
                {
                    "detail": f"Successfully unfollowed {profile_to_unfollow.user.username}."
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"detail": "You are not following this user."},
            status=status.HTTP_400_BAD_REQUEST,
        )
