from django import forms
from .models import Specific, Section, Education


class SectionFrom(forms.ModelForm):
    class Meta:
        model = Section
        fields = ('name', 'experiences')


class SpecificForm(forms.ModelForm):
    class Meta:
        model = Specific
        fields = ('image', 'description', 'bullet_section', 'section')


class EducationFrom(forms.ModelForm):
    class Meta:
        model = Education
        fields = ('image', 'location', 'certification_name', 'description', 'month', 'year', 'profile')
