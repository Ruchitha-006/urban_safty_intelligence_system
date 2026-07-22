from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """
    Additional information about each user.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    phone_number = models.CharField(
        max_length=15,
        blank=True
    )

    city = models.CharField(
        max_length=100,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.user.username