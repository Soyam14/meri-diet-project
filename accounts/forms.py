from django import forms
from django.contrib.auth.models import User
from .models import Profile

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

    def save(self, commit=True):
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        if commit:
            Profile.objects.create(
                user=user,
                phone_number=self.cleaned_data['phone_number']
            )
        return user