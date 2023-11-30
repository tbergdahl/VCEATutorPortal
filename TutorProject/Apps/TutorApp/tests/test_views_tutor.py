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
            password='MySpineIsntbroken123!',
            first_name='Jay',
            last_name='Cutler',
            is_tutor=True,
            is_student=False,
            is_admin=False
        )
        self.tutor_user.set_password('MySpineIsntbroken123!')
        self.tutor_user.save()

        # Create a student user
        self.student_user = CustomUser.objects.create(
            email='ronnie.coleman@wsu.edu',
            first_name='Ronnie',
            last_name='Coleman',
            is_student=True,
            is_tutor=False,
            is_admin=False
        ) 
        self.student_user.set_password('MySpineIsntbroken123!')
        self.student_user.save()
        # Create the tutor from the tutor user for testing
        self.tutor = Tutor(
            user=self.tutor_user,
            hours_tutored=0,
            day_started=None,
            rating=0.0,
            description='Legendary bodybuilder and actor'
        ) 
        # Create a tutor for testing
        self.major = Major.objects.create(name='Computer Science', abbreviation='CS')  
        self.major.save()

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
            start_time=timezone.now().time(),
            end_time=(timezone.now() + timedelta(hours=1)).time()
        ) 

        self.c.save() # saving here to prevend db error

        # Create a tutoring session for testing
        self.tutoring_session = TutoringSession.objects.create(
            tutor=self.tutor,
            student=self.student,
            start_time=timezone.now() + timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=1, minutes=20),
            tutored_class=self.c,
            description='Test tutoring session',
            shift=self.shift
            )
        # Create the TimeSlot objects
        start_time = time(7, 0)  
        end_time = time(21, 0)
        interval_minutes = 20

        current_time = start_time
        while current_time < end_time:
            try:
                TimeSlot.objects.get(start_time=current_time)
            except TimeSlot.DoesNotExist:
                TimeSlot.objects.create(start_time=current_time)
            current_time = (datetime.combine(datetime.today(), current_time) + timedelta(minutes=interval_minutes)).time()
        
        # Client initialization
        self.client = Client()
        self.tutor.save()
        self.student.save()
        self.shift.save()
        self.tutoring_session.save()

    def tearDown(self):
        # Clean up the created objects
        TutoringSession.objects.all().delete()
        Tutor.objects.all().delete()
        CustomUser.objects.all().delete()
        Class.objects.all().delete()
        Shift.objects.all().delete()
        TimeSlot.objects.all().delete()

# Tests for basic tutor views ###############################################################
    def test_tutor_view(self):
        # Log in the user and save all objects to database
        login_successful = self.client.login(email='jay.cutler1@wsu.edu', password='MySpineIsntbroken123!')

        # Check if the login was successful
        self.assertTrue(login_successful, "Login failed")

        # Access the tutor view
        response = self.client.get(reverse('Tutor:tutor_view'))

        # Check that the response is 200 OK and right template loaded
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutorPage.html')

        #logout and login as student and try to access tutor view
        self.client.logout()
        self.client.login(email='ronnie.coleman@wsu.edu', password='MySpineIsntbroken123!')

        #Try to login with invalid cridentials
        false_response = self.client.get(reverse('Tutor:tutor_view'))
        self.assertNotEqual(false_response.status_code, 302) # should fail
        
# Tests for tutor routes which view data
    def test_view_appointments(self):
        # Log in the user and save all objects to database
        login_successful = self.client.login(email='jay.cutler1@wsu.edu', password='MySpineIsntbroken123!')

        # Check if the login was successful
        self.assertTrue(login_successful, "Login failed")

        # Access the view_appointments view
        response = self.client.get(reverse('Tutor:view_appointments', args=[self.tutor.user.id]))

        # Check if the response is 200 OK and the right template is loaded
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutor_appointments.html')

    def test_cancel_appointment_view(self):
       # Log in as the tutor
        self.client.login(email='jay.cutler1@wsu.edu', password='MySpineIsntbroken123!')

        # Get the cancel appointment URL for the specific appointment
        cancel_url = reverse('Tutor:cancel_appointment', args=[self.tutoring_session.id])

        # Send a POST request to actually cancel the appointment
        response = self.client.post(cancel_url)

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check that the appointment is cancelled (student is None)
        self.tutoring_session.refresh_from_db()
        self.assertIsNone(self.tutoring_session.student)
        
# !!!! ISSUE WITH THIS TEST !!!! ##
    def test_appointment_completed_view(self):
        # Log in as the tutor
        self.client.login(email='jay.cutler1@wsu.edu', password='MySpineIsntbroken123!')

        # Get the appointment completed URL for the specific appointment
        completed_url = reverse('Tutor:appointment_completed', args=[self.tutoring_session.id])

        # Send a GET request to complete the appointment
        response = self.client.get(completed_url)

        # Check that the response status code is 302 (redirect)
        self.assertEqual(response.status_code, 302)

        # Check that the tutoring session is deleted
        with self.assertRaises(TutoringSession.DoesNotExist):
            self.tutoring_session.refresh_from_db()

        # Check that a redirect to view_appointments is performed
        self.assertRedirects(response, reverse('Tutor:view_appointments', args=[self.tutor.user_id]))