from django.db import transaction
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from pricing.models import UserSubscription
from users.permissions import IsAdmin

from .models import CancellationLog, YogaClass
from .serializers import YogaClassSerializer


class YogaClassListCreateAPI(generics.ListCreateAPIView):
    queryset = YogaClass.objects.all().order_by("start_at")
    serializer_class = YogaClassSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdmin()]
        return [permissions.AllowAny()]


class YogaClassDetailUpdateDeleteAPI(generics.RetrieveUpdateDestroyAPIView):
    queryset = YogaClass.objects.all()
    serializer_class = YogaClassSerializer

    def get_permissions(self):
        if self.request.method in ["PUT", "PATCH", "DELETE"]:
            return [IsAdmin()]
        return [permissions.AllowAny()]


class JoinClassAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        yoga_class = get_object_or_404(YogaClass, pk=pk)
        user = request.user

        # 1. Cek apakah user sudah terdaftar di kelas ini
        if yoga_class.participants.filter(id=user.id).exists():
            return Response(
                {"error": "Kamu sudah terdaftar di kelas ini!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 2. Cek kapasitas kelas
        if yoga_class.is_full:
            return Response(
                {"error": "Yah, kelas sudah penuh!"}, status=status.HTTP_400_BAD_REQUEST
            )

        # 3. Cek Subscription (Punya kredit gak?)
        # Kita cari subscription yang punya sisa kredit DAN masa aktifnya belum lewat
        active_sub = (
            UserSubscription.objects.filter(
                user=user,
                remaining_credits__gt=0,  # Kredit lebih dari 0
                expired_at__gt=timezone.now(),  # Belum kadaluarsa
            )
            .order_by("expired_at")
            .first()
        )  # Pakai yang mau expired duluan (biar hemat)

        if not active_sub:
            return Response(
                {"error": "Kamu tidak punya kredit aktif. Silakan beli paket dulu!"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 4. EKSEKUSI (Pakai Atomic Transaction)
        try:
            with transaction.atomic():
                # Kurangi kredit
                active_sub.remaining_credits -= 1
                active_sub.save()

                # Masukkan user ke kelas
                yoga_class.participants.add(user)

                return Response(
                    {
                        "message": "Berhasil join kelas!",
                        "class": yoga_class.name,
                        "remaining_credits": active_sub.remaining_credits,
                    },
                    status=status.HTTP_200_OK,
                )

        except Exception:
            return Response(
                {"error": "Terjadi kesalahan sistem saat memproses data."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


# classes/views.py


class MyJoinedClassesAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        status_param = request.query_params.get("status", "").strip("/").lower()
        now = timezone.now()

        # Kita pakai List biasa buat nampung gabungan data
        results = []
        if status_param != "cancelled":
            joined_qs = YogaClass.objects.filter(participants=user)

            # Filter Waktu (Opsional)
            if status_param == "upcoming":
                joined_qs = joined_qs.filter(start_at__gt=now)
            elif status_param == "history":
                joined_qs = joined_qs.filter(start_at__lt=now)

            # Masukkan ke list results
            for item in joined_qs:
                results.append(
                    {
                        "id": item.id,
                        "name": item.name,
                        "start_at": item.start_at,
                        "room": item.room,
                        "instructor_name": item.instructor_name,
                        "status": "JOINED",  # Status Aktif
                    }
                )
        if status_param == "cancelled" or status_param == "":
            cancelled_qs = CancellationLog.objects.filter(user=user).select_related(
                "yoga_class"
            )

            # Masukkan ke list results
            for log in cancelled_qs:
                results.append(
                    {
                        "id": log.yoga_class.id,
                        "name": log.yoga_class.name,
                        "start_at": log.yoga_class.start_at,
                        "room": log.yoga_class.room,
                        "instructor_name": log.instructor_name,
                        "status": "CANCELLED",  # Status Batal
                        "cancelled_at": log.cancelled_at,  # Ada tanggal cancel
                    }
                )

        results = sorted(results, key=lambda x: x["start_at"], reverse=True)

        return Response(results)


class CancelClassAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        yoga_class = get_object_or_404(YogaClass, pk=pk)
        user = request.user

        # 1. Cek apakah user terdaftar?
        if not yoga_class.participants.filter(id=user.id).exists():
            return Response({"error": "Kamu belum terdaftar di kelas ini."}, status=400)

        # 2. Hitung Waktu Mundur
        time_difference = yoga_class.start_at - timezone.now()
        hours_remaining = time_difference.total_seconds() / 3600

        # --- LOGIC STRICT DISINI ---

        # Kalau kurang dari 12 jam, LANGSUNG TOLAK.
        if hours_remaining < 12:
            return Response(
                {"error": "Maaf, pembatalan sudah ditutup."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 3. PROSES CANCEL NORMAL (Karena waktu masih aman)
        try:
            with transaction.atomic():
                # Hapus user dari kelas
                CancellationLog.objects.create(
                    user=user,
                    yoga_class=yoga_class,
                )

                yoga_class.participants.remove(user)

                # Refund Kredit
                active_sub = (
                    user.subscriptions.filter(expired_at__gt=timezone.now())
                    .order_by("-expired_at")
                    .first()
                )

                remaining = 0
                if active_sub:
                    active_sub.remaining_credits += 1
                    active_sub.save()
                    remaining = active_sub.remaining_credits

                return Response(
                    {
                        "message": "Cancel berhasil! Kredit kamu sudah dikembalikan.",
                        "remaining_credits": remaining,
                    },
                    status=status.HTTP_200_OK,
                )

        except Exception as e:
            return Response({"error": str(e)}, status=500)
