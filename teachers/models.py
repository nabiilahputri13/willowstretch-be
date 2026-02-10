from django.db import models


class Teacher(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to="teachers/")
    bio = models.TextField()
    specialty = models.CharField(max_length=100)
    certification = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-created_at"]
