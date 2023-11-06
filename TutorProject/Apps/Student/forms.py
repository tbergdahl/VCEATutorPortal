from django import forms
from Apps.TutorApp.models import Tutor, Session
from django.utils import timezone

class TutorRatingForm(forms.ModelForm):
    class Meta:
        model = Tutor
        fields = ['rating', 'description']
        
class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['date', 'time']

    def clean_date(self):
        date = self.cleaned_data['date']
        if date < timezone.now().date():
            raise forms.ValidationError("The date cannot be in the past!")
        if date > timezone.now().date() + timezone.timedelta(days=14):
            raise forms.ValidationError("You can only book a session up to 14 days in advance.")
        return date