from rest_framework import serializers

from .models import YogaClass


class YogaClassSerializer(serializers.ModelSerializer):
    is_booked_by_user = serializers.SerializerMethodField()
    is_full = serializers.BooleanField(read_only=True)
    participant_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = YogaClass
        fields = [
            "id",
            "name",
            "instructor_name",
            "start_at",
            "duration_minutes",
            "max_capacity",
            "room",
            "participants",  # List ID user yang join
            "participant_count",
            "is_full",
            "created_at",
            "is_booked_by_user"
        ]
        # Agar saat create kelas, kita ga dipaksa masukin participants
        extra_kwargs = {"participants": {"read_only": True}}

    def get_is_booked_by_user(self, obj):
        # Ambil user dari context request
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # Cek apakah user login ini ada di dalam participants kelas ini
            return obj.participants.filter(id=request.user.id).exists()
        return False
