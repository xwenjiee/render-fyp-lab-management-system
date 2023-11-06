from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data.get("email", "")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError((f"{email} is taken."), params={"email": email})
        return email

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


# class UserUpdateForm(PasswordChangeForm):
#     # def clean_email(self):
#     #     email = self.cleaned_data.get("email", "")
#     #     if User.objects.filter(email=email).exists():
#     #         raise forms.ValidationError((f"{email} is taken."), params={"email": email})
#     #     return email

#     class Meta:
#         model = User
#         fields = ["password1", "password2"]


# class ProfileUpdateForm(forms.ModelForm):
#     class Meta:
#         model = User
#         fields = ["username", "email"]
