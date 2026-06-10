from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema
from rest_framework import generics, viewsets, mixins, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from user.serializers import LogoutSerializer, UserRegisterSerializer, ProfileSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from user.models import Profile
from utils.permissions import IsOwnerOrReadOnly


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = get_user_model().objects.all()
    permission_classes = (AllowAny,)


class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ProfileViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Profile.objects.select_related("user").prefetch_related(
        "followers",
        "following",
    )
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = [SearchFilter]
    search_fields = ["user__username", "bio"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def follow(self, request, pk=None):
        profile_to_follow = self.get_object()
        current_profile = Profile.objects.filter(user=request.user).first()

        if current_profile is None:
            return Response(
                {"detail": "Create your profile before following users."},
                status=status.HTTP_400_BAD_REQUEST,
            )

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

    @extend_schema(
        summary="Follow a user profile",
        description="Allows the authenticated user to follow another user's profile.",
        responses={200: dict, 400: dict},
    )
    @action(detail=True, methods=["POST"], permission_classes=[IsAuthenticated])
    def unfollow(self, request, pk=None):
        profile_to_unfollow = self.get_object()
        current_profile = Profile.objects.filter(user=request.user).first()

        if current_profile is None:
            return Response(
                {"detail": "Create your profile before unfollowing users."},
                status=status.HTTP_400_BAD_REQUEST,
            )

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
