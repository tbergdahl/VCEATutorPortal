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
from django.contrib.auth import get_user_model

warnings.filterwarnings("ignore")

class AdminViewsTest(TestCase):
# Setup and Teardown methods ##############################
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
        self.major = Major.objects.create(name='Computer Science', abbreviation='CS')  # Assuming you have Major model defined
        self.major.save()

        self.c = Class(
            class_major=self.major,
            course_num=101,
            course_name="Intro to Programming",
            hours_tutored=0,
        )
        self.c.save()

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
            hours_tutored=0,
            day_started=None,
            rating=0.0,
            description='Legendary bodybuilder and actor',
            major=self.major
        )
        self.tutor.save()

        # Create a shift for testing
        self.shift = Shift.objects.create(
            tutor=self.tutor,
            day='Monday',
            start_time=time(8, 0),  # 8:00 AM
            end_time=time(9, 0)    # 9:00 AM
        )
        self.shift.save()

    def teardown(self):
        # Clean up the created objects
        Tutor.objects.all().delete()
        CustomUser.objects.all().delete()
        Major.objects.all().delete()
        Class.objects.all().delete()
        Shift.objects.all().delete()

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
        login = self.client.login(email='admin@example.com', password='password123')

        # Check if the login was successful
        self.assertTrue(login, "Login failed")

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
        self.assertEqual(self.tutor.shifts.count(), 2)

        # Get the shift ID
        shift_id = self.tutor_shift.id

        # Access the admin_delete_shift view
        response = self.client.post(reverse('Admin:admin_delete_shift', args=[shift_id]))

        # Check if the shift is deleted
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after deletion
        self.assertEqual(self.tutor.shifts.count(), 1)

    def test_admin_add_tutor_shift(self):
        #Log in admin
        self.client.login(email='admin@example.com', password='password123')
        # Ensure no shifts exist initially
        self.assertEqual(Shift.objects.count(), 1)
        # Create a valid form data for the shiftform
        form_data = {
            'day': 'Monday',
            'start_time': '08:00',
            'end_time': '09:00',
        }
        # Access the admin_add_tutor_shift view with a POST request
        response = self.client.post(reverse('Admin:admin_add_tutor_shift', args=[self.tutor.user_id]), data=form_data)
        # Check if the shift is created
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after creation
        self.assertEqual(Shift.objects.count(), 2)
        # Check the attributes of the created shift
        created_shift = Shift.objects.first()
        self.assertEqual(created_shift.tutor, self.tutor)
        self.assertEqual(created_shift.day, 'Monday')
        self.assertEqual(created_shift.start_time.strftime('%H:%M'), '08:00')
        self.assertEqual(created_shift.end_time.strftime('%H:%M'), '09:00')
        # Ensure the string representation is correct
        self.assertEqual(str(created_shift), 'Monday from 08:00 AM to 09:00 AM')

    def test_admin_view_tutor_shifts(self):
        # Log in admin
        self.client.login(email='admin@example.com', password='password123')

        # Assuming self.tutor is an instance of Tutor
        response = self.client.get(reverse('Admin:admin_view_tutor_shifts', args=[self.tutor.user_id]))

        # Check if the response status code is 200 (OK)
        self.assertEqual(response.status_code, 200)

        shift = self.tutor.shifts.first()

        #print("Response content:", response.content.decode())
        self.assertContains(response, shift.day)
        self.assertContains(response, '8 a.m.')
        self.assertContains(response, '9 a.m.')

    def test_admin_edit_tutor_profile(self):
        # Log in admin
        self.client.login(email='admin@example.com', password='password123')

        form_data = { # Must contain every single field
            'major': self.major.id,
            'tutored_classes': [self.c.id],  # Pass the actual Class instance ID
            'description': 'UpdatedDescription',
            'hours_tutored': 0,  # Add hours_tutored field
            'first_name': 'Dorian',  # Change first_name
            'last_name': 'Yates',  # Change last_name
        }
        # Access the admin_edit_tutor_profile view
        response = self.client.post(reverse('Admin:admin_edit_tutor_profile', args=[self.tutor.user_id]), data=form_data)

        # Check if the tutor profile is updated
        self.assertEqual(response.status_code, 200)  # Assuming it returns a success status code
        self.tutor.refresh_from_db()

        # Check if the tutor profile is updated
        self.assertEqual(self.tutor.description, 'UpdatedDescription')
        self.assertEqual(self.tutor.major, self.major)
        self.assertEqual(self.tutor, self.c.available_tutors.first())
        self.assertEqual(self.tutor.user.first_name, 'Dorian')
        self.assertEqual(self.tutor.user.last_name, 'Yates')

# Test Major and Class Delete / Create ##############################
    def test_delete_major(self):
        # login the admin
        self.client.login(email='admin@example.com', password='password123')
        # Ensure a major is created
        self.assertEqual(Major.objects.count(), 1)
        # Get the major ID
        major_id = self.major.id
        # Access the delete_major view
        response = self.client.post(reverse('Admin:delete_major', args=[major_id]))
        # Check if the major is deleted
        self.assertEqual(response.status_code, 302)  # Assuming it redirects after deletion
        self.assertEqual(Major.objects.count(), 0)

    def test_delete_class(self):
        self.client.login(email='admin@example.com', password='password123')
        self.assertEqual(Class.objects.count(), 1)
        class_id = self.c.id
        response = self.client.post(reverse('Admin:delete_class', args=[class_id]))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Class.objects.count(), 0)

    def test_admin_create_major(self):
        # login the admin
        self.client.login(email='admin@example.com', password='password123')
        # Ensure no majors exist initially
        self.assertEqual(Major.objects.count(), 1)
        # Create a valid form data
        form_data = {
            'name': 'Computer Science',
            'abbreviation': 'CS'
        }
        # Access the admin_create_major view with a POST request
        response = self.client.post(reverse('Admin:admin_create_major'), data=form_data)
        # Check if the major is created
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Major.objects.count(), 2)

    def test_admin_create_class(self):
        # login the admin
        self.client.login(email='admin@example.com', password='password123')
        # Ensure only 1 classes exist initially (The class in the setup function)
        self.assertEqual(Class.objects.count(), 1)
        # Create a valid form data
        form_data = {
            'class_major': self.major.id,
            'course_num': 101,
            'course_name': 'Intro to Programming',
            'hours_tutored': 0,
        }
        # Access the admin_create_class view with a POST request
        response = self.client.post(reverse('Admin:admin_create_class'), data=form_data)
        # Check if the class is created
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Class.objects.count(), 2)
        # Check the attributes of the created class
        created_class = Class.objects.first()
        self.assertEqual(created_class.class_major, self.major)
        self.assertEqual(created_class.course_num, 101)
        self.assertEqual(created_class.course_name, 'Intro to Programming')
        self.assertEqual(created_class.hours_tutored, 0)

# Test menu views of class and major for Admin ##############################
    def test_majors_menu(self):
        # login the admin
        self.client.login(email='admin@example.com', password='password123')                 
        # Create some majors for testing
        major1 = Major.objects.create(name='Computer Science', abbreviation='CS')
        major2 = Major.objects.create(name='Electrical Engineering', abbreviation='EE')
        # Access the majors_menu view
        response = self.client.get(reverse('Admin:majors_menu'))  # Adjust the URL name based on your project configuration
        # Check if the response status code is successful
        self.assertEqual(response.status_code, 200)
        # Check if the majors are present in the response context
        self.assertIn(major1, response.context['majors'])
        self.assertIn(major2, response.context['majors'])
        # Check if the rendered HTML contains major names
        self.assertContains(response, 'Computer Science')
        self.assertContains(response, 'Electrical Engineering')

    def test_classes_menu(self):
        # login the admin
        self.client.login(email='admin@example.com', password='password123')
        # Test route
        response = self.client.get(reverse('Admin:classes_menu'))
        self.assertEqual(response.status_code, 200)  # Check that successful response code is sent
        # Test content of response
        self.assertIn(self.c, response.context['classes'])
        # Test that rendered HTML contains class names
        self.assertContains(response, 'Intro to Programming')


    
