from django import forms
from django.contrib.auth import get_user_model 
from django.contrib.auth.forms import UserCreationForm

class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=12, min_length=4, required=True, help_text="Required: First Name")
    last_name = forms.CharField(max_length=12, min_length=4, required=True, help_text="Required: Last Name")
    email = forms.EmailField(required=True, help_text="Required: Email Address")

    class Meta:
        model = get_user_model()
        fields = ("username", "first_name", "last_name", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"] 
        
        if commit:
            user.save()
        return user

class UserLoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput)
