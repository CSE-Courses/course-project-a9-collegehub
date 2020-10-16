from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class initRegisterForm(UserCreationForm):
     email = forms.EmailField(required = True)

     class Meta:
         model = User
         fields = ['username', 'email', 'password']
from .models import Specific


class SpecificForm(forms.ModelForm):
    class Meta:
        model = Specific
        fields = ('image', 'description', 'bullet_section', 'section')
