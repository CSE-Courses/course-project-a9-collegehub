from django import forms
from .models import Specific


class SpecificForm(forms.ModelForm):
    class Meta:
        model = Specific
        fields = ('image', 'description', 'bullet_section', 'section')
