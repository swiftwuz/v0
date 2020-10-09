from django import forms
# from django.contrib.auth.forms import UserCreationForm

from .models import Admin, Profile, Institution


class InstRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput
    )

    class Meta:
        model = Institution
        fields = ['email', 'password', 'password2']

        def clean_mail(self):
            email = self.cleaned_data.get('email')
            queryset = Institution.objects.filter(email='email')
            if queryset.exist():
                raise forms.ValidationError("Email already taken.")
            return email

        def clean_password(self):
            password = self.cleaned_data.get('password')
            password2 = self.cleaned_data.get('password2')
            if password and password2 and password != password2:
                raise forms.ValidationError("Passwords do not match.")
            return password2


class AdminRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput
    )

    class Meta:
        model = Admin
        fields = ['username', 'email', 'password', 'password2']

        def clean_mail(self):
            email = self.cleaned_data.get('email')
            queryset = Admin.objects.filter(email='email')
            if queryset.exist():
                raise forms.ValidationError("Email already taken.")
            return email

        def clean_password(self):
            password = self.cleaned_data.get('password')
            password2 = self.cleaned_data.get('password2')
            if password and password2 and password != password2:
                raise forms.ValidationError("Passwords do not match.")
            return password2

        def save(self, commit=True):
            admin = super().save(commit=False)
            admin.set_password(self.cleaned_data.get['password'])
            if commit:
                admin.save()


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = Admin
        fields = ('email', 'username')


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('image',)
