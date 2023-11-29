# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from Apps.TutorApp.models import *
from Apps.TutorApp.forms import *
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
import warnings
from django.utils import timezone, dateformat
from datetime import datetime, time
from django.core.exceptions import ValidationError

warnings.filterwarnings("ignore")

class TutorViewsTest(TestCase):
# Setup and Teardown methods for tutor view testing ##########################################
    def setUp(self):
        # Create a test user
        self.tutor_user = CustomUser.objects.create(
            email='jay.cutler1@wsu.edu',
            first_name='Jay',
            last_name='Cutler',
            is_tutor=True,
            is_student=False,
            is_admin=False
        )
        # Create a student user
        self.student_user = CustomUser.objects.create(
            email='ronnie.coleman@wsu.edu',
            first_name='Ronnie',
            last_name='Coleman',
            is_student=True,
            is_tutor=False,
            is_admin=False
        ) 
        # Create the tutor from the tutor user for testing
        self.tutor = Tutor(
            user=self.tutor_user,
            hours_tutored=0,
            day_started=None,
            rating=0.0,
            description='Legendary bodybuilder and actor'
        ) 
        # create a student from the student user for testing
        self.student = Student(user=self.student_user)
        # Create a class for view interactions
        self.c = Class(
            class_major=self.major,
            course_num=101,
            course_name="Intro to Programming",
            hours_tutored=0,
        ) 
        # Create a shift for shift interaction
        self.shift = Shift.objects.create(
            tutor=self.tutor,
            day='Monday',
            start_time=time(8, 0),  # 8:00 AM
            end_time=time(9, 0)    # 9:00 AM
        ) 
        # Client initialization
        self.client = Client()
        self.tutor.save()
        self.student.save()
        self.c.save()
        self.shift.save()
    
    def tearDown(self):
        # Clean up the created objects
        Tutor.objects.all().delete()
        CustomUser.objects.all().delete()
        Class.objects.all().delete()
        Shift.objects.all().delete()

# Tests for basic tutor views
    def test_tutor_view(self):
        # Log in the user and save all objects to database
        self.client.login(email='jay.cutler1@wsu.edu', password='MySpineIsntbroken')

        # Access the tutor view
        response = self.client.get(reverse('Tutor:tutor_view'))

        # Check that the response is 200 OK and right template loaded
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutorPage.html')
        
# Tests for tutor routes which view data
    def test_view_appointments(self):
        # Log in the user and save all objects to the database
        self.client.login(email='jay.cutler1@wsu.edu', password='MySpineIsntbroken')

        # Access the view_appointments view
        response = self.client.get(reverse('view_appointments', args=[self.tutor.id]))

        # Check if the response is 200 OK and the right template is loaded
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutor_appointments.html')

