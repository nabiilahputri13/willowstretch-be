from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    is_admin: models.BooleanField = models.BooleanField(
        default=False
    )  # Untuk membedakan Admin & User biasa

    USERNAME_FIELD = "email"  # Login pakai email, bukan username
    REQUIRED_FIELDS = ["username"]
