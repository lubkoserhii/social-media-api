from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from user.views import CreateUserView, ProfileViewSet

router = DefaultRouter()
router.register("profiles", ProfileViewSet, basename="profile")
urlpatterns = [
    path("register/", CreateUserView.as_view(), name="register"),
    # Ендпоінт для логіну (передаємо email + password, отримуємо access та refresh токени)
    path("login/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    # Ендпоінт для оновлення access-токена за допомогою refresh-токена
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include(router.urls)),
]

app_name = "user"
