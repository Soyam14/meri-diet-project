from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import AuthenticationForm # Make sure this is imported
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
import random
from .forms import CustomSignUpForm, DietitianSignUpForm, OTPForm
from .models import User, Profile, DietitianProfile

# --- Signup and OTP Process ---

def signup_choice_view(request):
    return render(request, 'accounts/signup_choice.html')

def user_signup_view(request):
    if request.method == 'POST':
        form = CustomSignUpForm(request.POST)
        if form.is_valid():
            otp = random.randint(100000, 999999)
            send_mail(
                'Your MERI DIET Account Verification Code',
                f'Your OTP to complete your registration is: {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [form.cleaned_data['email']],
            )
            request.session['signup_data'] = request.POST
            request.session['otp'] = otp
            request.session['signup_type'] = 'user'
            return redirect('verify_otp')
    else:
        form = CustomSignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def dietitian_signup_view(request):
    if request.method == 'POST':
        form = DietitianSignUpForm(request.POST)
        if form.is_valid():
            otp = random.randint(100000, 999999)
            send_mail(
                'Your MERI DIET Dietitian Account Verification',
                f'Your OTP to complete your dietitian registration is: {otp}',
                settings.DEFAULT_FROM_EMAIL,
                [form.cleaned_data['email']],
            )
            request.session['signup_data'] = request.POST
            request.session['otp'] = otp
            request.session['signup_type'] = 'dietitian'
            return redirect('verify_otp')
    else:
        form = DietitianSignUpForm()
    return render(request, 'accounts/dietitian_signup.html', {'form': form})

@transaction.atomic
def verify_otp_view(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid():
            saved_otp = request.session.get('otp')
            entered_otp = int(form.cleaned_data['otp'])

            if saved_otp == entered_otp:
                signup_data = request.session.get('signup_data')
                signup_type = request.session.get('signup_type')
                
                form_class = CustomSignUpForm if signup_type == 'user' else DietitianSignUpForm
                
                signup_form = form_class(signup_data)
                if signup_form.is_valid():
                    user = signup_form.save(commit=False) # Create user object without saving yet
                    user.is_active = True # Activate the user
                    user.save() # Now save the user
                    
                    # Create Profile and DietitianProfile
                    profile = Profile.objects.create(
                        user=user,
                        phone_number=signup_form.cleaned_data['phone_number'],
                        is_dietitian=(signup_type == 'dietitian')
                    )
                    if signup_type == 'dietitian':
                        DietitianProfile.objects.create(
                            user=user,
                            specialization=signup_form.cleaned_data['specialization'],
                            bio=signup_form.cleaned_data.get('bio', '')
                        )
                    
                    del request.session['signup_data']
                    del request.session['otp']
                    del request.session['signup_type']
                    login(request, user)
                    
                    if profile.is_dietitian:
                        return redirect('dietitian_dashboard')
                    else:
                        return redirect('dashboard')
            else:
                return render(request, 'accounts/verify_otp.html', {'form': form, 'error': 'Invalid OTP. Please try again.'})
    
    return render(request, 'accounts/verify_otp.html', {'form': OTPForm()})

    
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