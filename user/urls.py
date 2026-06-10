from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from user.serializers import UserTokenObtainPairSerializer
from user.views import CreateUserView, LogoutView, ProfileViewSet

router = DefaultRouter()
router.register("profiles", ProfileViewSet, basename="profile")

urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    path(
        "login/",
        TokenObtainPairView.as_view(serializer_class=UserTokenObtainPairSerializer),
        name="token_obtain_pair",
    ),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]

app_name = "user"
