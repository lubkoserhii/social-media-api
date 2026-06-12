from django.contrib.auth.base_user import AbstractBaseUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import Token


class TokenVersionJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token: Token) -> AbstractBaseUser:
        user = super().get_user(validated_token)

        if validated_token.get("token_version", 0) != user.token_version:
            raise AuthenticationFailed(
                "Token has been revoked.",
                code="token_not_valid",
            )

        return user
