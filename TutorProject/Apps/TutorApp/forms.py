from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from Apps.TutorApp.models import *



class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


class AdminCreateUser(UserCreationForm):
    ROLE_CHOICES = [
        ('is_student', 'Student'),
        ('is_tutor', 'Tutor'),
        ('is_admin', 'Admin'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2', 'role')

class PDFSelectionForm(forms.Form):
    REPORT_CHOICES = [
        ('report1', 'Tutor Statistics Report'),
        ('report2', 'Tutoring Hours By Class'),
        ('report3', 'Tutor Statistic Report'),
    ]
    report = forms.ChoiceField(choices=REPORT_CHOICES, label='Select Report')

class ClassCreationForm(forms.ModelForm):
    class Meta:
        model = Class
        fields = ['classmajor', 'coursenum']

class MajorCreationForm(forms.ModelForm):
    class Meta:
        model = Major
        fields = ['name']