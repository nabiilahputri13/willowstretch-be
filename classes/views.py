from rest_framework import generics, permissions

from users.permissions import IsAdmin

from .models import YogaClass
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
