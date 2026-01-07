from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import datetime
import jwt

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = User.objects.filter(email=email).first()

        if user is None:
            raise AuthenticationFailed('User tidak ketemu!')

        if not user.check_password(password):
            raise AuthenticationFailed('Password salah!')

        # Payload: Isi dari kartu identitas (token)
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()

        # SIMPAN TOKEN DI COOKIE
        response.set_cookie(key='jwt', value=token, httponly=True) # httponly biar aman dari hacker
        response.data = {
            'message': 'Login Berhasil!',
            'is_admin': user.is_admin
        }
        return response

class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {'message': 'Logout Berhasil'}
        return response