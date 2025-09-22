# planner/admin.py
from django.contrib import admin
from .models import DietPlan, PreMadePlan

admin.site.register(DietPlan)
admin.site.register(PreMadePlan)