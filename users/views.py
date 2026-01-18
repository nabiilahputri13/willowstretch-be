from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer


class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        user = authenticate(email=email, password=password)

        if user is None:
            return Response({"error": "Email/Password salah"}, status=401)

        # GENERATE TOKEN PAKAI SIMPLEJWT
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)  # Ini token masuknya

        response = Response()

        # Simpan di Cookie dengan nama 'access_token' (sesuai authentication.py)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            samesite="Lax",
            secure=False,  # Ubah True kalau production (HTTPS)
        )

        response.data = {"message": "Login Berhasil!", "is_admin": user.is_admin}
        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        # Hapus cookie yang namanya 'access_token'
        response.delete_cookie("access_token")
        response.data = {"message": "Logout Berhasil"}
        return response
