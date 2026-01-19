from django.db import models

class Package(models.Model):
    name = models.CharField(max_length=100) # Misal: "Starter Pack", "Monthly Unlimited"
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    credits = models.PositiveIntegerField(help_text="Berapa banyak sesi yoga yang didapat?")
    duration_days = models.PositiveIntegerField(help_text="Masa aktif paket dalam hari")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - Rp{self.price}"

class UserSubscription(models.Model):
    # Menghubungkan paket yang dibeli dengan user
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="subscriptions")
    package = models.ForeignKey(Package, on_delete=models.PROTECT)
    remaining_credits = models.PositiveIntegerField()
    expired_at = models.DateTimeField()
    bought_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.package.name}"

    @property
    def is_active(self):
        from django.utils import timezone
        return self.remaining_credits > 0 and self.expired_at > timezone.now()