# meridiet/urls.py
from planner.views import debug_view
from django.contrib import admin
from django.urls import path, include
from planner.views import home_view

urlpatterns = [
    path('what-is-my-real-host-name-debug/', debug_view, name='debug_view'),
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),  # Homepage ka URL
    path('accounts/', include('accounts.urls')), # accounts app ke saare URLs yahan se handle honge
    path('planner/', include('planner.urls')), # planner app ke saare URLs yahan se handle honge
] 