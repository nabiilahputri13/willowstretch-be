from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import UserSerializer  # Import serializer yang tadi dibuat


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

        # GENERATE TOKEN
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        response = Response()

        # 1. Set Cookie (Hanya bisa dibaca server, aman dari XSS)
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            samesite="Lax",
            secure=False,  # Ubah True jika pakai HTTPS (Production)
        )

        # 2. Serialize User Data
        # Ini langkah penting agar Frontend tahu dia Admin atau bukan
        user_data = UserSerializer(user).data

        # 3. Return Response Body
        # Kita kirim token juga di body untuk State Management (Pinia)
        response.data = {"message": "Login Berhasil!", "access": access_token, "user": user_data}

        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie("access_token")
        response.data = {"message": "Logout Berhasil"}
        return response
