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
            is_admin=True,
            is_student=False,
            is_tutor=False
        )
        self.tutor_user = CustomUser.objects.create(
            email='jay.cutler@wsu.edu',
            first_name='Jay',
            last_name='Cutler',
            is_tutor=True,
            is_student=False,
            is_admin=False
        )
        self.student_user = CustomUser.objects.create(
            email='ronnie.coleman@wsu.edu',
            first_name='Ronnie',
            last_name='Coleman',
            is_student=True,
            is_tutor=False,
            is_admin=False
        )

    def test_dummy(self):
        self.assertEqual(True, True)

    def test_Admin(self):
        # Create the Admin and associate it with the CustomUser
        admin = Admin(user=self.admin_user)

        # Test admin assignment
        self.assertTrue(admin.user.is_admin)
        self.assertFalse(admin.user.is_student)
        self.assertFalse(admin.user.is_tutor)

    def test_Tutor(self):
        # Create the Tutor and associate it with the CustomUser
        tutor = Tutor(
            user=self.tutor_user,
            minutes_tutored=0,
            day_started=None,
            rating=0.0,
            description='Legendary bodybuilder and actor'
        )

        # Test tutor assignment
        self.assertFalse(tutor.user.is_student)
        self.assertFalse(tutor.user.is_admin)
        self.assertTrue(tutor.user.is_tutor)

    def test_Student(self):
        # Create student from setUp student_user
        student = Student(user=self.student_user)

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
        u = CustomUser(
            email='rich.piana@wsu.edu',
            first_name='Rich',
            last_name='Piana'
        )
        u.set_password('testing123')
        self.assertFalse(u.check_password('testing234'))  # Test incorrect password
        self.assertTrue(u.check_password('testing123'))  # Test correct password

    def test_class_model(self):
       # Create the Tutor and associate it with the CustomUser
        self.tutor_test = CustomUser(
            email='sergi@wsu.edu',
            first_name='Sergi',
            last_name='Oliva',
            is_tutor=True,
            is_student=False,
            is_admin=False
        )

        self.T = Tutor(
            user=self.tutor_test,
            minutes_tutored=0,
            day_started=None,
            rating=0.0,
            description='Legendary bodybuilder and Baki Character'
        )

        # Create a Class
        self.M = Major(name="Computer Science", abbreviation="CS")

        self.c = Class(
            class_major=self.M,
            course_num=101,
            course_name="Intro to Programming",
            hours_tutored=0,
        )

        # Test Class Information
        self.assertEqual(self.c.course_name, "Intro to Programming")
        self.assertEqual(self.c.class_major.name, "Computer Science")
        self.assertEqual(self.c.class_major.abbreviation, "CS")
        self.assertEqual(self.c.course_num, 101)
        self.assertEqual(self.c.hours_tutored, 0)