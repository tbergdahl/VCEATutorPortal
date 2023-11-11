from django import forms
from Apps.TutorApp.models import Tutor, TutoringSession
from django.utils import timezone

class TutorRatingForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ['rating', 'description']
        