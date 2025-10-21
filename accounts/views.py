# MyDietApp/accounts/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.db import transaction
from .forms import CustomSignUpForm
from .models import Profile, User

@transaction.atomic
def signup_view(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # This is the fix for the IntegrityError.
            # It creates the Profile associated with the new user.
            Profile.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number']
            )
            
            login(request, user)
            return redirect('home')
    else:
        form = CustomSignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('home')

def secret_admin_signup_view(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            # This creates a user who is also an admin/superuser
            user = User.objects.create_superuser(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            # Create their profile
            Profile.objects.create(
                user=user,
                phone_number=form.cleaned_data['phone_number']
            )
            login(request, user)
            return redirect('/admin/') # Redirect to the admin page after creation
    else:
        form = CustomSignUpForm()
    # We will create the template for this in the next step
    return render(request, 'accounts/secret_admin_signup.html', {'form': form})

