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
from django.core.signing import TimestampSigner, BadSignature
from django.core.mail import send_mail, outbox
from django.core import mail
from Apps.Student.views import send_email

warnings.filterwarnings("ignore")

class StudentViewsTest(TestCase):
# Setup and Teardown methods for student view testing ##########################################
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
            description='Legendary bodybuilder and actor',
            token = '1234567890'
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
        self.c.save() # saving here to prevend db error
        self.c.available_tutors.add(self.tutor)
        self.c.save()

        # Create a shift for shift interaction
        self.shift = Shift.objects.create(
            tutor=self.tutor,
            day='Monday',
            start_time=timezone.now().time(),
            end_time=(timezone.now() + timedelta(hours=1)).time()
        ) 

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
        Student.objects.all().delete()
        Tutor.objects.all().delete()
        CustomUser.objects.all().delete()
        Class.objects.all().delete()
        Shift.objects.all().delete()
        TimeSlot.objects.all().delete()
        Major.objects.all().delete()

# Test Basic student View #######################################################################

    def test_student_view(self):        
        # Log in the student user
        self.client.login(email='ronnie.coleman@wsu.edu', password='MySpineIsntbroken123!')

        # Access the student view without student logged in
        response = self.client.get(reverse('Student:student_view'))

        # Check that the response is 200 OK and the right template is loaded
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'studentPage.html')

        self.client.logout()

        #Log in another type of user
        self.client.login(email='jay.cutler1@wsu.edu', password='MySpineIsntbroken123!')

        response = self.client.get(reverse('Student:student_view'))

        # Check that the response isnt 200
        self.assertNotEqual(response.status_code, 200)

# Test Student Rating Tutor  ####################################################################
    #@unittest.skip("Skip this test to control the execution order")
    def test_student_rate_tutor_view(self):  #Tests the get method
        # Log in the student user
        login_successful = self.client.login(email='ronnie.coleman@wsu.edu', password='MySpineIsntbroken123!')
        self.assertTrue(login_successful, "Login failed")

        # Generate a signed token for a specific tutor
        signer = TimestampSigner()
        signed_token = signer.sign(f"rate_tutor_1")

        # Test Get Request Method
        response_get = self.client.get(reverse('Student:rate_tutor', args=[signed_token]))

        # Check that the response is 200 O
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'feedback_form.html')

        # Test POST Request Method
        response_post = self.client.post(reverse('Student:rate_tutor', args=[signed_token]), {
            'rating': 5,  # Provide the required form data
            'feedback': 'Great tutor!',
        })

        # Check that the response is an HTTP response with the expected message
        self.assertEqual(response_post.status_code, 200)
        self.assertEqual(response_post.content.decode(), "Thanks For Your Feedback!")

        # For example, assuming your Feedback model has a 'rating' field:
        feedback = Feedback.objects.first()
        self.assertEqual(feedback.rating, 5)  # Check if the rating was saved

    def test_book_appointment(self):  # for some reason when run before test_rate_tutor_view causes error
        # Log in the student user
        login_successful = self.client.login(email='ronnie.coleman@wsu.edu', password='MySpineIsntbroken123!')
        self.assertTrue(login_successful, "Login failed")

        # Access the book_appointment view (GET request)
        response_get = self.client.get(reverse('Student:book_appointment', args=[self.tutoring_session.id]))
        # Check that the response is 200 OK and the right template is loaded
        self.assertEqual(response_get.status_code, 200)
        self.assertTemplateUsed(response_get, 'book_appointment.html')

        # Post request
        response_post = self.client.post(reverse('Student:book_appointment', args=[self.tutoring_session.id]), {
            'tutored_class': self.c.id,  # Provide the required form data
            'description': 'Test description',  # Include the description field
        })

        # Check that the response is a redirect to the student_view_appointments page
        self.assertRedirects(response_post, reverse('Student:student_view_appointments', args=[self.student.user_id]))
        self.tutoring_session.refresh_from_db()
        self.assertEqual(self.tutoring_session.student, self.student)

    def test_student_view_tutor(self):
        # Log in the student user
        login_successful = self.client.login(email='ronnie.coleman@wsu.edu', password='MySpineIsntbroken123!')
        self.assertTrue(login_successful, "Login failed")

        # Access the student_view_tutors view
        response = self.client.get(reverse('Student:student_view_tutors', args=[self.tutor.user.id]))

        # Check that the response is 200 OK and the right template is loaded
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tutor_available_appointments.html')

        #print (response.content)

        #Check that response contains information about the tutor
        self.assertContains(response, self.tutor.user.first_name)
        self.assertContains(response, self.tutor.user.last_name)
        #self.assertContains(response, self.email)

        #print("Available Appointments:", response.context.get('available_appointments'))

    def test_student_view_appointments(self):
        #Login the user
        login_successful = self.client.login(email='ronnie.coleman@wsu.edu', password='MySpineIsntbroken123!')
        self.assertTrue(login_successful, "Login failed")

        response = self.client.get(reverse('Student:student_view_appointments', args=[self.student.user.id]))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'student_appointments.html')

        self.assertEqual(response.context['student'], self.student)
        self.assertIn('appointments', response.context)

        expected_appointments = TutoringSession.objects.filter(student=self.student)
        self.assertQuerysetEqual(response.context['appointments'], expected_appointments, transform=lambda x: x)
    
    def test_student_cancel_appointment(self):
        # Log in the student user
        login_successful = self.client.login(email='ronnie.coleman@wsu.edu', password='MySpineIsntbroken123!')
        self.assertTrue(login_successful, "Login failed")

        # Create a tutoring session for the student
        tutoring_session = TutoringSession.objects.create(
            tutor=self.tutor,
            student=self.student,
            start_time=timezone.now() + timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=1, minutes=20),
            tutored_class=self.c,
            description='Gucci Gang Gucci Gang Gucci Gang',
            shift=self.shift
        )

        # Access the cancel_appointment view
        response = self.client.get(reverse('Student:cancel_appointment', args=[tutoring_session.id]))

        # Check that the response is a redirect to the student_view_appointments page
        self.assertRedirects(response, reverse('Student:student_view_appointments', args=[self.student.user_id]))

        # Refresh and check that student is None
        tutoring_session.refresh_from_db()
        self.assertIsNone(tutoring_session.student)
        
    def test_send_email(self):
        # Log in the student user
        login_successful = self.client.login(email='ronnie.coleman@wsu.edu', password='MySpineIsntbroken123!')
        self.assertTrue(login_successful, "Login failed")

        # Create a tutoring session
        tutoring_session = TutoringSession.objects.create(
            tutor=self.tutor,
            student=self.student,
            start_time=timezone.now() + timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=1, minutes=20),
            tutored_class=self.c,
            description='Test tutoring session',
            shift=self.shift
        )
        # send email using view function
        send_email(tutoring_session)

        # print("email sent")
        # Check that an email was sent
        self.assertEqual(len(mail.outbox), 1)

        # Check content
        # print(mail.outbox)
        sent_email = mail.outbox[0]
        self.assertIn('Your Appointment', sent_email.subject)
        self.assertIn('You have an appointment with Jay Cutler at', sent_email.body)
    
