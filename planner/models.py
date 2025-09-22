# planner/models.py
from django.db import models
from django.contrib.auth.models import User

# Model No. 1: User ke personal saved diet plans ke liye
class DietPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    plan_details = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Plan for {self.user.username}: {self.title}"

# Model No. 2: Pehle se bane hue diet charts ke liye
class PreMadePlan(models.Model):
    title = models.CharField(max_length=200)
    details = models.TextField()
    
    def __str__(self):
        return self.title