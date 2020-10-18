from django import forms
from .models import Specific
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Specific, Section, Education


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('name',)


class SignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')


class SpecificForm(forms.ModelForm):
    class Meta:
        model = Specific
        fields = ('title', 'image', 'description', 'bullet_section', 'section', 'link')


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ('image', 'location', 'certification_name', 'description', 'month', 'year', 'profile')
