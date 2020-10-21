from django import forms
from django.forms import ValidationError
from users.models import User

from .models import Profile


class AdminRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

        def clean_password(self):
            password = self.cleaned_data["password"]
            confirm_password = self.cleaned_data["password2"]
            if password != confirm_password:
                raise forms.ValidationError("Password mismatch!")
            return confirm_password


class AdminLoginForm(forms.ModelForm):
    email = forms.EmailField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["email", "password"]

    def check_email(self):
        email = self.cleaned_data["email"]
        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise ValidationError("You entered an incorrect password")

        if not user.is_active:
            raise ValidationError("This user is not active.")
        return email

    def check_password(self):
        password = self.cleaned_data.get["password"]
        User.objects.filter(password__iexact=password).exists()
        if not password:
            raise ValidationError("Entered incorrect password.")
        return password


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('email', 'username')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)
