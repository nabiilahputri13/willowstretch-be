from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "is_admin"]
        extra_kwargs = {"password": {"write_only": True}}  # Password gak boleh dipamerin/dibaca

    def create(self, validated_data):
        # Hash password biar gak kebaca orang
        password = validated_data.pop("password", None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
