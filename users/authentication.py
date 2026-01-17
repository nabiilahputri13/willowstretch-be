from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request: Request):
        # Pastikan nama kuncinya sama dengan yang di LoginView ('access_token')
        raw_token = request.COOKIES.get("access_token")
        if not raw_token:
            return None
        try:
            validated_token = self.get_validated_token(raw_token)
        except (InvalidToken, TokenError, AuthenticationFailed):
            return None
        return self.get_user(validated_token), validated_token
