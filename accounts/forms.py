from django import forms
from django.contrib.auth.models import User
from .models import Profile, DietitianProfile

class CustomSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    phone_number = forms.CharField(max_length=15)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
            
        if User.objects.filter(email=cleaned_data.get('email')).exists():
            raise forms.ValidationError("An account with this email already exists.")

class DietitianSignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    phone_number = forms.CharField(max_length=15)
    email = forms.EmailField(required=True)
    specialization = forms.CharField(max_length=100)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'phone_number', 'password', 'specialization', 'bio']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")
        if User.objects.filter(email=cleaned_data.get('email')).exists():
            raise forms.ValidationError("An account with this email already exists.")

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, min_length=6, required=True)