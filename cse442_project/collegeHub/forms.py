from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

 class initRegisterForm(UserCreationForm):
     email = forms.EmailField(required = True)

     class Meta:
         model = User
         fields = ['username', 'email', 'password']
