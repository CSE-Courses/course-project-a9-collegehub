from django import forms
from .models import Specific
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Specific, Section, Education, UserProfile
from django.contrib.auth.forms import UserCreationForm
from .models import Specific, Section, Education, Skill, Project


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('name',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'profile_pic', 'occupation', 'location', 'github', 'linkedin', 'instagram','resume', 'quote' ,)


class UserEditForm(UserChangeForm):
    password = None

    class Meta:
        fields = ("username", "first_name","last_name", "email",)
        model = get_user_model()


class SignupForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs['placeholder'] = "Username"
        self.fields["username"].widget.attrs['id'] = "signup_Username"
        self.fields["username"].widget.attrs['class'] = "form-control grey_field"

        self.fields["email"].widget.attrs['placeholder'] = "Email address"
        self.fields["email"].widget.attrs['class'] = "form-control grey_field"

        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['first_name'].widget.attrs['class'] = 'form-control grey_field'

        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['last_name'].widget.attrs['class'] = 'form-control grey_field'

        self.fields['password1'].widget.attrs['placeholder'] = 'Password (Min. 8 Characters)'
        self.fields['password1'].widget.attrs['class'] = 'form-control grey_field'

        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].widget.attrs['class'] = 'form-control grey_field'


class SpecificForm(forms.ModelForm):
    class Meta:
        model = Specific
        fields = ('position', 'company', 'description', 'link')


class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ('institution', 'certification_name', 'description', 'month', 'year')


class SkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = ('name', )


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'month', 'year')

