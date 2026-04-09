from datetime import timedelta

from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response

from users.permissions import IsAdmin  # Permission custom kamu

from .models import Package, UserSubscription
from .serializers import PackageSerializer, UserSubscriptionSerializer


# 1. List & Create Package (Admin only create, Public read)
class PackageListCreateAPI(generics.ListCreateAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdmin()]  # Cuma Admin boleh bikin harga
        return [permissions.AllowAny()]  # User biasa boleh liat harga


# 2. Detail Package (Update/Delete Admin Only)
class PackageDetailAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [IsAdmin]


# 3. Buy Package (Simulasi Pembelian)
class BuyPackageAPI(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, package_id):
        # Ambil paket yang mau dibeli
        package = get_object_or_404(Package, id=package_id)
        user = request.user

        # Hitung kapan kadaluarsanya
        expiry_date = timezone.now() + timedelta(days=package.duration_days)

        # Buat Subscription baru buat user
        subscription = UserSubscription.objects.create(
            user=user,
            package=package,
            remaining_credits=package.credits,
            expired_at=expiry_date,
        )

        serializer = UserSubscriptionSerializer(subscription)
        return Response(
            {"message": "Paket berhasil dibeli!", "data": serializer.data},
            status=status.HTTP_201_CREATED,
        )


# 4. Lihat Subscription Saya
class MySubscriptionListAPI(generics.ListAPIView):
    serializer_class = UserSubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Filter cuma punya user yang login
        return UserSubscription.objects.filter(user=self.request.user).order_by(
            "-bought_at"
        )
