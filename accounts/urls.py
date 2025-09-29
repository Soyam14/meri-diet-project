from django.urls import path
from .views import (
    user_signup_view, 
    login_view, 
    logout_view,
    dietitian_signup_view,
    signup_choice_view,
    verify_otp_view
)

urlpatterns = [
    # Renamed the old 'signup' to 'user_signup' for clarity
    path('signup/user/', user_signup_view, name='user_signup'),
    
    # New URLs for the signup process
    path('signup/', signup_choice_view, name='signup_choice'),
    path('signup/dietitian/', dietitian_signup_view, name='dietitian_signup'),
    path('verify-otp/', verify_otp_view, name='verify_otp'),
    
    # Existing URLs
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    # We will add dietitian dashboard and other URLs later
]