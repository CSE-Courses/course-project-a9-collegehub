from django import forms
<<<<<<< HEAD
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class initRegisterForm(UserCreationForm):
     email = forms.EmailField(required = True)

     class Meta:
         model = User
         fields = ['username', 'email', 'password']
=======
from .models import Specific


class SpecificForm(forms.ModelForm):
    class Meta:
        model = Specific
        fields = ('image', 'description', 'bullet_section', 'section')
>>>>>>> ca2ba7a9e20dc6f9013f11fa9e80a6fef7283bd8
