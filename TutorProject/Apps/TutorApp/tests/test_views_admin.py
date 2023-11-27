from django.test import TestCase, Client
from django.urls import reverse
from Apps.TutorApp.models import *
from Apps.TutorApp.forms import *
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
import warnings
from django.utils import timezone, dateformat
from datetime import datetime, time

warnings.filterwarnings("ignore")

class AdminViewsTest(TestCase):
    def setUp(self):
        # Create an admin user
        self.admin_user = get_user_model().objects.create_user(
            email='admin@example.com',
            password='password123',
            is_admin=True,
            is_student=False,
            is_tutor=False
        )
        self.client = Client()

        # Create a tutor for testing
        major = Major.objects.create(name='Computer Science', abbreviation='CS')  # Assuming you have Major model defined

        # Create a test user
        self.tutor_user = CustomUser.objects.create(
            email='jay.cutler1@wsu.edu',
            first_name='Jay',
            last_name='Cutler',
            is_tutor=True,
            is_student=False,
            is_admin=False
        )

        # Create a new Tutor instance for each test
        self.tutor = Tutor(
            user=self.tutor_user,
            minutes_tutored=0,
            day_started=None,
            rating=0.0,
            description='Legendary bodybuilder and actor',
            major=major
        )
        self.tutor.save()
# Test Admin Basic View ##############################
    def test_admin_view(self):
        # Log in the admin user
        self.client.login(email='admin@example.com', password='password123')

        # Access the admin view
        response = self.client.get(reverse('Admin:admin_view'))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'adminPage.html')

# Test Admin User Creation ##############################
    def test_admin_create_user(self):
        # Log in the admin user
        self.client.login(email='admin@example.com', password='password123')

        # Access the admin create user view
        response = self.client.get(reverse('Admin:admin_create_user'))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'createuser.html')

        # Simulate form to Successfully create a new user 
        new_user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'newuser@example.com',
            'password1': 'newpassword123',
            'password2': 'newpassword123',
            'role': 'is_student',  # Change role based on your form
        }
        # Create a user data form that will fail to be created
        fail_user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': ''
        }

        response = self.client.post(reverse('Admin:admin_create_user'), data=new_user_data)
        fail_response = self.client.post(reverse('Admin:admin_create_user'), data=fail_user_data)

        # Check if the form submission was successful
        self.assertEqual(response.status_code, 302)  # 302 indicates a redirect after successful form submission
        self.assertNotEqual(fail_response.status_code, 302)  # 302 not equal indicates failed re-direct after form submission

        # Check if the user was created successfully
        self.assertTrue(get_user_model().objects.filter(email='newuser@example.com').exists())

# Test User Deletion ##############################
    def test_admin_delete_user_success(self):
        # Log in the admin user
        self.client.login(email='admin@example.com', password='password123')

        # Create a user to be deleted
        user_to_delete = get_user_model().objects.create_user(
            email='user_to_delete@example.com',
            password='userpassword',
            is_admin=False,
            is_student=True,
            is_tutor=False
        )

        # Access the admin delete user view
        response = self.client.get(reverse('Admin:admin_delete_user'))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'deleteUser.html')

        # Simulate form submission to delete the user
        response = self.client.post(reverse('Admin:admin_delete_user'), {'user_id': user_to_delete.id})

        # Check if the user was deleted successfully
        self.assertFalse(get_user_model().objects.filter(id=user_to_delete.id).exists())

        # Check success message in messages
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('User deleted successfully.', messages)

    def test_admin_delete_user_failure(self):
        # Log in the admin user
        self.client.login(email='admin@example.com', password='password123')

        # Create a user that cannot be deleted (is_admin=True)
        user_not_to_delete = get_user_model().objects.create_user(
            email='not_to_delete@example.com',
            password='userpassword',
            is_admin=True,
            is_student=False,
            is_tutor=False
        )

        # Simulate form submission to delete the user (which should fail)
        response = self.client.post(reverse('Admin:admin_delete_user'), {'user_id': user_not_to_delete.id})

        # Check if the user was not deleted
        self.assertTrue(get_user_model().objects.filter(id=user_not_to_delete.id).exists())

        # Check error message in messages
        messages = [m.message for m in get_messages(response.wsgi_request)]
        self.assertIn('Cannot delete another admin.', messages)

# Test PDF functionality ##############################
# Needs testing for form types added later
    def test_render_form(self):
        # Login the admin
        self.client.login(email='admin@example.com', password='password123')

        # Perform a GET request to render the initial form
        response = self.client.get(reverse('Admin:admin_view_reports'))

        # Check if the response is successful
        self.assertEqual(response.status_code, 200)

    def test_pdf_preview(self):
        # Log in the admin user
        self.client.login(email='admin@example.com', password='password123')

        # Make a GET request for PDF preview
        response = self.client.get(reverse('Admin:pdf_preview'), {'report_type': 'report1'})

        # Check if the response is a PDF data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')

# Test View of Tutors ##############################
    def test_admin_view_tutors(self):
        # Log in the admin user
        self.client.login(email='admin@example.com', password='password123')

        # Access the admin view
        response = self.client.get(reverse('Admin:admin_view_tutors'))  # Use the correct view_name
        self.assertEqual(response.status_code, 200)  # Assuming the view_name is correct and accessible to the admin

        # Check if the expected tutor information is present in the response
        testuser = self.tutor_user
        self.assertContains(response, 'Jay Cutler')  # Check for tutor's name

# Test Scheduling of Admin ##############################
    def test_admin_delete_shift(self):
        # login the admin
        self.client.login(email='admin@example.com', password='password123')

        # Create a test shift for the tutor
        self.tutor_shift = Shift.objects.create(
            tutor=self.tutor,
            day='Monday',
            start_time=time(8, 0),  # 8:00 AM
            end_time=time(9, 0)    # 9:00 AM
        )

        self.tutor_shift.save()

        # Ensure a shift is created for the tutor
        self.assertEqual(self.tutor.shifts.count(), 1)

        # Get the shift ID
        shift_id = self.tutor_shift.id

        # Access the admin_delete_shift view
        response = self.client.post(reverse('Admin:admin_delete_shift', args=[shift_id]))

        # Check if the shift is deleted
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after deletion
        self.assertEqual(self.tutor.shifts.count(), 0)

    def test_admin_add_tutor_shift(self):
        pass
    def test_admin_view_tutor_shifts(self):
        pass    

# Test Major and Class Interactions ##############################
    def test_delete_major(self):
        pass
    def test_delete_class(self):
        pass
    def test_admin_create_major(self):
        pass
    def test_admin_create_class(self):
        pass   
    def test_majors_menu(self):
        pass
    def test_classes_menu(self):
        pass

    
