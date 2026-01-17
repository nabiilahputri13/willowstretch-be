from rest_framework import serializers

from .models import YogaClass


class YogaClassSerializer(serializers.ModelSerializer):
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
        ]
        # Agar saat create kelas, kita ga dipaksa masukin participants
        extra_kwargs = {"participants": {"read_only": True}}
