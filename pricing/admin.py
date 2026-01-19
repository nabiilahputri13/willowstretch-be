from django.contrib import admin
from .models import Package, UserSubscription

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'credits', 'duration_days')

@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'package', 'remaining_credits', 'expired_at', 'is_active')
    list_filter = ('package',)