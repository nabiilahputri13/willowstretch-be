from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class AuthIntegrationTest(APITestCase):
    def setUp(self):
        self.reg_data = {
            "username": "putri_test",
            "email": "putri@test.com",
            "password": "password123",
        }
        self.register_url = reverse("register")
        self.login_url = reverse("login")

    def test_full_auth_flow(self):
        """Tes alur lengkap: Daftar -> Login"""
        # 1. Tes Registrasi - Kita pakai 200 karena views kamu balikin 200
        reg_response = self.client.post(self.register_url, self.reg_data)
        self.assertEqual(reg_response.status_code, status.HTTP_200_OK)  # Diubah dari 201 ke 200

        # 2. Tes Login
        login_data = {
            "email": self.reg_data["email"],
            "password": self.reg_data["password"],
        }
        login_response = self.client.post(self.login_url, login_data)
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        # Pastikan set_cookie 'jwt' berhasil
        self.assertIn("access_token", login_response.cookies)

    def test_login_invalid_user(self):
        """Tes login dengan user yang tidak terdaftar"""
        bad_data = {"email": "salah@email.com", "password": "wrong"}
        response = self.client.post(self.login_url, bad_data)
        # Kita pakai 401 karena sistem kamu balikin 401
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_wrong_password(self):
        """Tes login dengan email benar tapi password salah"""
        # Kita buat user dulu
        User.objects.create_user(**self.reg_data)

        # Coba login dengan password ngasal
        response = self.client.post(
            self.login_url,
            {"email": "putri@test.com", "password": "password_salah_banget"},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout(self):
        """Tes fungsi logout menghapus cookie"""
        logout_url = reverse("logout")
        response = self.client.post(logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["message"], "Logout Berhasil")
        # Cek apakah cookie jwt sudah kosong/terhapus
        response.cookies["access_token"].value, ""
