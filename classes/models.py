from django.db import models

from users.models import User  # Kita ambil User dari app users kamu


class YogaClass(models.Model):
    name = models.CharField(max_length=100)
    instructor_name = models.CharField(max_length=100)
    start_at = models.DateTimeField()
    duration_minutes = models.PositiveIntegerField(default=60)
    max_capacity = models.PositiveIntegerField()
    room = models.CharField(max_length=50)
    participants = models.ManyToManyField(User, related_name="joined_classes", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # Biar nama kelasnya muncul enak dibaca di Admin
    def __str__(self):
        return f"{self.name} ({self.start_at.strftime('%d %b %H:%M')})"

    # Hitung isFull otomatis
    @property
    def is_full(self):
        return self.participants.count() >= self.max_capacity

    @property
    def participant_count(self):
        return self.participants.count()


class CancellationLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    yoga_class = models.ForeignKey(YogaClass, on_delete=models.CASCADE)
    cancelled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Log: {self.user.username} cancel {self.yoga_class.name}"
