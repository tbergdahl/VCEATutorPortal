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
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, initial='is_student')


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
        fields = ['class_major', 'course_num', 'course_name']
        labels = {
            'class_major': 'Major',
            'course_num': 'Course Number',
            'course_name': 'Course Name'
        }

class MajorCreationForm(forms.ModelForm):
    class Meta:
        model = Major
        fields = ['name', 'abbreviation']
        labels = {
            'name': 'Name of Major',
            'abbreviation': 'Abbreviation (i.e CPT_S)'
        }

class EditTutorForm(forms.ModelForm): 

    tutored_classes = forms.ModelMultipleChoiceField(
        queryset=Class.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False  
    )

    major = forms.ModelChoiceField(queryset=Major.objects.all())

    class Meta:
        model = Tutor
        fields = ['major', 'minutes_tutored', 'description', 'tutored_classes']

    def __init__(self, *args, **kwargs):
        super(EditTutorForm, self).__init__(*args, **kwargs)

        if self.instance.user:
            self.fields['first_name'] = forms.CharField(initial=self.instance.user.first_name)
            self.fields['last_name'] = forms.CharField(initial=self.instance.user.last_name)


class ShiftForm(forms.ModelForm):
    day_choices = [
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    ]

    day = forms.ChoiceField(choices=day_choices)
    start_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    end_time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    class Meta:
        model = Shift
        fields = ['day', 'start_time', 'end_time']
