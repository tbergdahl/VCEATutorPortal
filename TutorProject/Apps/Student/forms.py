from django import forms
from Apps.TutorApp.models import Tutor

class TutorRatingForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ['rating', 'description']