from django.urls import path
# Add the new view to the import list
from .views import signup_view, login_view, logout_view, secret_admin_signup_view

urlpatterns = [
    # This is your new secret path. Place it at the top.
    path('create-my-secret-admin-account-now/', secret_admin_signup_view, name='secret_admin_signup'),
    
    # Your other URLs
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
