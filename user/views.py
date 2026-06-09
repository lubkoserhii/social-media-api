from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework.permissions import AllowAny
from user.serializers import UserRegisterSerializer


class CreateUserView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
    queryset = get_user_model().objects.all()
    permission_classes = (AllowAny,)
