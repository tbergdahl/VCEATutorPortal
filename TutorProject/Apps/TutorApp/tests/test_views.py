# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from Apps.TutorApp.models import *
from django.test import TestCase
from django.test import Client
import warnings

warnings.filterwarnings("ignore")
        
# Test cases for views
class ViewsTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()

        # Create a test users with various roles for testing
        self.admin_user = CustomUser(
            email='phil.health@wsu.edu',
            first_name='Admin',
            last_name='User',
            is_admin=True,
            is_student=False,
            is_tutor=False
        )
        self.tutor_user = CustomUser(
            email='jay.cutler@wsu.edu',
            first_name='Jay',
            last_name='Cutler',
            is_tutor=True,
            is_student=False,
            is_admin=False
        )
        self.student_user = CustomUser(
            email='ronnie.coleman@wsu.edu',
            first_name='Ronnie',
            last_name='Coleman',
            is_student=True,
            is_tutor=False,
            is_admin=False
        )
        #create admin, tutor, and student from test users
        self.admin = Admin(user=self.admin_user)
        self.tutor = Tutor(
            user=self.tutor_user,
            minutes_tutored=0,
            day_started=None,
            rating=0.0,
            description='Legendary bodybuilder and actor'
        )
        self.student = Student(user=self.student_user)

    def tearDown(self):
        # Delete the created objects to clean up
        CustomUser.objects.all().delete()
        Admin.objects.all().delete()
        Tutor.objects.all().delete()
        Student.objects.all().delete()


    def test_login_admin(self):
        self.client.login(username='phil.health@wsu.edu', password='mr_olympia_2008')
        self.assertEqual(self.admin_user.is_admin, True)
        response = self.client.get(reverse('Admin:admin_view')) # get simulates a GET request, reverse finds the url by name
        self.assertEqual(response.status_code, 200)  # 200 is the HTTP status code for "OK"
        self.assertTemplateUsed(response, 'adminPage.html')  # Asserts that the template used to render the response was studentPage.html


    # def test_login_tutor(self):
    #     self.client.login(username='jay.cutler@wsu.edu', password='mr_olympia_2009')
    #     response = self.client.get(reverse('Tutor:tutor_view')) # get simulates a GET request, reverse finds the url by name
    #     self.assertEqual(response.status_code, 200)  # 200 is the HTTP status code for "OK"
    #     self.assertTemplateUsed(response, 'tutorPage.html')  # Asserts that the template used to render the response was studentPage.html


    # def login_student(self):
    #     self.client.login(username='ronnie.coleman@wsu.edu', password='mr_olympia_20010')
    #     response = self.client.get(reverse('Student:student_view')) # get simulates a GET request, reverse finds the url by name
    #     self.assertEqual(response.status_code, 200)  # 200 is the HTTP status code for "OK"
    #     self.assertTemplateUsed(response, 'studentPage.html')  # Asserts that the template used to render the response was studentPage.html

    # def test_admin_view_createuser(self):

    #     self.client.login(username='phil.health@wsu.edu', password='mr_olympia_2008')
    #     self.assertEqual(self.admin_user.is_admin, True)

    #     response = self.client.get(reverse('Admin:admin_create_user'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'createuser.html')

    # def test_admin_view_deleteuser(self):
    #     self.login_admin()
    #     response = self.client.get(reverse('Admin:admin_delete_user'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'deleteUser.html')

    # Test student, tutor, and admin views
    # def test_student_view(self):
    #     response = self.client.get(reverse('student_view')) # get simulates a GET request, reverse finds the url by name
    #     self.assertEqual(response.status_code, 200)  # 200 is the HTTP status code for "OK"
    #     self.assertTemplateUsed(response, 'studentPage.html')  # Asserts that the template used to render the response was studentPage.html

    # def test_tutor_view(self):
    #     response = self.client.get(reverse('tutor_view'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'tutorPage.html')

    # # Test home view
    # def test_home_authenticated_admin(self):
    #     # Simulate an authenticated admin user
    #     user = CustomUser.objects.create(email='admin@example.com', is_admin=True)
    #     self.client.force_login(user)

    #     response = self.client.get(reverse('home'))
    #     self.assertEqual(response.status_code, 302)  # Redirects to admin_view

    # def test_home_authenticated_student(self):
    #     # Simulate an authenticated student user
    #     user = CustomUser.objects.create(email='student@example.com', is_student=True)
    #     self.client.force_login(user)

    #     response = self.client.get(reverse('home'))
    #     self.assertEqual(response.status_code, 302)  # Redirects to student_view

    # def test_home_authenticated_tutor(self):
    #     # Simulate an authenticated tutor user
    #     user = CustomUser.objects.create(email='tutor@example.com', is_tutor=True)
    #     self.client.force_login(user)

    #     response = self.client.get(reverse('home'))
    #     self.assertEqual(response.status_code, 302)  # Redirects to tutor_view

    # def test_home_unauthenticated(self):
    #     response = self.client.get(reverse('home'))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'login.html')

    # Test Register view
    # def test_register(self):
    #     Setting Request
    #     response = self.client.post(reverse('register'), {
    #         'email': 'test@example',
    #         'first_name': 'test',
    #         'last_name': 'user',
    #         'password1': 'Test_password_complex_123',
    #         'password2': 'Test_password_complex_123',
    #        'is_student': True }
    #      
    #     # Testing Results
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'register.html')
    #     self.assertContains(response, '')