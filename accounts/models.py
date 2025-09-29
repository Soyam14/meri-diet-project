from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True)
    is_premium = models.BooleanField(default=False)
    is_dietitian = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class DietitianProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100, default='General Nutrition')
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Dietitian: {self.user.username}"