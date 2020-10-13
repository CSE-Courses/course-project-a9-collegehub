from django import forms
from .models import Specific
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm


class SignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username','first_name', 'last_name', 'email', 'password1', 'password2')

class SpecificForm(forms.ModelForm):
    class Meta:
        model = Specific
        fields = ('image', 'description', 'bullet_section', 'section')
