from django import forms
from .models import Specific
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from .models import Specific, Section, Education, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.admin import widgets

from .models import Specific, Section, Education, Skill, Project, Event


class UserPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordResetForm, self).__init__(*args, **kwargs)
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
        'class': 'form-control grey_field',
        'placeholder': 'Email',
        'type': 'email',
        'name': 'email'
        }))

class SetPasswordForm(forms.Form):
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput(attrs={'class':'form-control grey_field' }))
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput(attrs={'class':'form-control grey_field'}))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(SetPasswordForm, self).__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user

class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('name',)

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('title', 'start_time', 'end_time', 'notes')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["title"].widget.attrs['id'] = "event_form_title"
        self.fields["title"].widget.attrs['class'] = "form-control grey_field"
        self.fields["notes"].widget.attrs['id'] = "event_form_title"
        self.fields["notes"].widget.attrs['class'] = "form-control grey_field"
        self.fields["start_time"].widget.attrs['class'] = "form-control grey_field"
        self.fields["end_time"].widget.attrs['class'] = "form-control grey_field"

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('bio', 'occupation', 'location', 'github', 'linkedin', 'instagram', 'phone_number', 'age', 'profile_pic','resume')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["bio"].widget.attrs['placeholder'] = "Tell me about Yourself"
        self.fields["bio"].widget.attrs['id'] = "bio"
        self.fields["bio"].widget.attrs['class'] = "form-control grey_field"
        self.fields["occupation"].widget.attrs['class'] = "form-control grey_field"
        self.fields['location'].widget.attrs['placeholder'] = 'Where Do you live?'
        self.fields['location'].widget.attrs['class'] = 'form-control grey_field'
        self.fields['phone_number'].widget.attrs['class'] = 'form-control grey_field'
        self.fields['age'].widget.attrs['class'] = 'form-control grey_field'
        self.fields['github'].widget.attrs['class'] = 'form-control grey_field'
        self.fields['instagram'].widget.attrs['class'] = 'form-control grey_field'
        self.fields['linkedin'].widget.attrs['class'] = 'form-control grey_field'
        self.fields['profile_pic'].widget.attrs['class'] = 'custom-file-input'
        self.fields['resume'].widget.attrs['class'] = 'custom-file-input'
        self.fields['profile_pic'].widget.attrs['id'] = 'inputGroupFile01'
        self.fields['resume'].widget.attrs['id'] = 'inputGroupFile02'


class UserEditForm(UserChangeForm):
    password = None

    class Meta:
        fields = ("username", "first_name", "last_name", "email",)
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields["username"].widget.attrs['class'] = "form-control grey_field_account"
        self.fields["username"].widget.attrs['id'] = "id_username_account"
        self.fields["first_name"].widget.attrs['class'] = "form-control grey_field_account"
        self.fields['last_name'].widget.attrs['class'] = 'form-control grey_field_account'
        self.fields['email'].widget.attrs['class'] = 'form-control grey_field_account'
     
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


class DeleteSpecificForm(forms.ModelForm):
    class Meta:
        model = Specific
        fields = []

class DeleteSectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = []

class DeleteEducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = []

class DeleteSkillForm(forms.ModelForm):
    class Meta:
        model = Skill
        fields = []

class DeleteProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = []

class ChooseTemplateForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = []