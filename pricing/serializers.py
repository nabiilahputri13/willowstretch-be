from rest_framework import serializers
from .models import Package, UserSubscription

class PackageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Package
        fields = "__all__"

class UserSubscriptionSerializer(serializers.ModelSerializer):
    # Kita tampilin detail paketnya, bukan cuma ID-nya doang
    package_name = serializers.CharField(source="package.name", read_only=True)
    
    class Meta:
        model = UserSubscription
        fields = [
            "id", 
            "package", 
            "package_name", 
            "remaining_credits", 
            "expired_at", 
            "bought_at", 
            "is_active"
        ]
        read_only_fields = ["expired_at", "bought_at", "remaining_credits"]