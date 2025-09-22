# planner/urls.py
from django.urls import path
from .views import (
    dashboard_view, 
    chatbot_view, 
    save_chatbot_plan_view,
    plans_list_view,
    add_premade_plan_view,
    terms_and_conditions_view,
    privacy_policy_view,
    support_view,
    delete_plan_view
)

urlpatterns = [
    path('dashboard/', dashboard_view, name='dashboard'),
    path('delete-plan/<int:plan_id>/', delete_plan_view, name='delete_plan'),
    path('chatbot/', chatbot_view, name='chatbot'),
    path('save-chatbot-plan/', save_chatbot_plan_view, name='save_chatbot_plan'),
    path('plans/', plans_list_view, name='plans_list'),
    path('add-premade-plan/<int:plan_id>/', add_premade_plan_view, name='add_premade_plan'),
    path('terms-and-conditions/', terms_and_conditions_view, name='terms_and_conditions'),
    path('privacy-policy/', privacy_policy_view, name='privacy_policy'),
    path('support/', support_view, name='support'),
]