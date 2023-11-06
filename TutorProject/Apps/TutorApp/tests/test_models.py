import warnings
import os
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from Apps.TutorApp.models import *  # Import your models from the correct location

warnings.filterwarnings("ignore")

class TestConfig(TestCase):
    @override_settings(TESTING=True)  # Use the override_settings decorator to set TESTING to True
    def test_test_config(self):
        self.assertEqual(True, True)  # Add a simple test

class TestModels(TestCase):

    def setUp(self):
        # Create a test user for each role
        self.admin_user = CustomUser.objects.create(
            email='phil.health@wsu.edu',
            first_name='Admin',
            last_name='User',
            is_admin=True
        )
        self.tutor_user = CustomUser.objects.create(
            email='jay.cutler@wsu.edu',
            first_name='Jay',
            last_name='Cutler',
            is_tutor=True
        )
        self.student_user = CustomUser.objects.create(
            email='ronnie.coleman@wsu.edu',
            first_name='Ronnie',
            last_name='Coleman',
            is_student=True
        )

    def test_Admin(self):
        # Create the Admin and associate it with the CustomUser
        admin = Admin.objects.create(user=self.admin_user)

        # Test admin assignment
        self.assertTrue(admin.user.is_admin)
        self.assertFalse(admin.user.is_student)
        self.assertFalse(admin.user.is_tutor)


    def test_Tutor(self):
        # Create the Tutor and associate it with the CustomUser
        tutor = Tutor.objects.create(
            user=self.tutor_user,
            minutes_tutored=0,
            day_started=None,
            rating=0.0,
            description='Legendary bodybuilder and actor'
        )

        # Test tutor assignment
        self.assertTrue(tutor.user.is_tutor)
        self.assertFalse(tutor.user.is_student)
        self.assertFalse(tutor.user.is_admin)

    def test_Student(self):
        # Create student from setUp student_user
        student = Student.objects.create(user=self.student_user)

        # Test student assignment
        self.assertTrue(student.user.is_student)
        self.assertFalse(student.user.is_tutor)
        self.assertFalse(student.user.is_admin)

    def tearDown(self):
        # Delete the created objects to clean up
        CustomUser.objects.all().delete()
        Admin.objects.all().delete()
        Tutor.objects.all().delete()
        Student.objects.all().delete()

    def test_password_hashing(self):
        u = CustomUser.objects.create(
            email='rich.piana@wsu.edu',
            first_name='Rich',
            last_name='Piana'
        )
        u.set_password('testing123')
        self.assertFalse(u.check_password('testing234'))  # Test incorrect password
        self.assertTrue(u.check_password('testing123'))  # Test correct password

    def test_class_model(self):
        # Test Course model by creating a course object and checking its title
        M = Major.objects.create(name = "Computer Science", abbreviation = "CS")

        # Create the Tutor and associate it with the CustomUser
        tutor = Tutor.objects.create(
            user=self.tutor_user,
            minutes_tutored=0,
            day_started=None,
            rating=0.0,
            description='Legendary bodybuilder and actor'
        )
        
        # create class object
        c = Class.objects.create(
            course_num=101,
            class_major=M,
            course_name="Intro to Programming",
            hours_tutored=0
        )

        c.availableTutors.add(tutor)
        c.save()

        # Test Class Information
        self.assertEqual(c.course_name, "Intro to Programming")
        self.assertEqual(c.class_major.name, "Computer Science")
        self.assertEqual(c.class_major.abbreviation, "CS")
        self.assertEqual(c.course_num, 101)
        self.assertEqual(c.hours_tutored, 0)

        # Test Tutor Information
        self.assertEqual(c.availableTutors.first().user.email, "jay.cutler@wsu.edu")
        self.assertEqual(c.availableTutors.first().user.first_name, "Jay")
        self.assertEqual(c.availableTutors.first().user.last_name, "Cutler")

        # Test Tutor assignment
        self.assertEqual(c.availableTutors.first().user.is_student, False)
        self.assertEqual(c.availableTutors.first().user.is_tutor, True)
        self.assertEqual(c.availableTutors.first().user.is_admin, False)

"""
    def test_verification_testing(self):
        client = Client()

        # Test student login and logout
        client.login(username='Ronnie', password='test_password')
        response = client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

        # Test Admin login and Logout
        client.login(username='Arnold', password='test_password')
        response = client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

        # Test Tutor login and Logout
        client.login(username='Jay', password='test_password')
        response = client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

    def test_appointment_deletion(self):
        pass

    def test_appointment_update(self):
        pass
"""