import warnings
import os
from datetime import time
from django.test import TestCase, Client, override_settings
from django.urls import reverse
from django.utils import timezone
from Apps.TutorApp.models import *  # Import your models from the correct location

warnings.filterwarnings("ignore")

class TestConfig(TestCase):
    @override_settings(TESTING=True)  # Use the override_settings decorator to set TESTING to True
    def test_test_config(self):
        self.assertEqual(True, True)  # Add a simple test

class TestModels(TestCase):

    def setUp(self):
        # Create a test user
        self.user = CustomUser.objects.create(
            email='chris.bumstead@wsu.edu',
            first_name='Chris',
            last_name='Bumstead',
            is_tutor=False,
            is_student=True,
            is_admin=False
        )
        # Create a test tutor user
        self.tutor_user = CustomUser.objects.create(
            email='jay.cutler1@wsu.edu',
            first_name='Jay',
            last_name='Cutler',
            is_tutor=True,
            is_student=False,
            is_admin=False
        )
        #Create test tutor
        self.tutor = Tutor(
            user=self.tutor_user,
            hours_tutored=0,
            day_started=None,
            rating=0.0,
            description='Legendary bodybuilder and actor'
        )
        self.user.save()
        self.tutor.save()

# Testing Password Methods
    def test_password_hashing(self):
        u = CustomUser(
            email='rich.piana@wsu.edu',
            first_name='Rich',
            last_name='Piana'
        )
        u.set_password('testing123')
        self.assertFalse(u.check_password('testing234'))  # Test incorrect password
        self.assertTrue(u.check_password('testing123'))  # Test correct password

    def test_password_reset_code_creation(self):
        # Create a Password Reset Code instance
        reset_code = PasswordResetCode.objects.create(user=self.user)

        # Check if the code is generated
        self.assertIsNotNone(reset_code.code)
        self.assertEqual(len(reset_code.code), 6) #Make sure code is correct length

        # Check if created_at is set to the current time
        self.assertIsNotNone(reset_code.created_at)
        self.assertTrue(timezone.now() - reset_code.created_at < timezone.timedelta(seconds=1))

        # Check the __str__ method
        expected_str = f"Password reset code for {self.user.email}"
        self.assertEqual(str(reset_code), expected_str)

# Testing Class, Major, and Shifts
def test_class_model(self):
    # Create the Tutor and associate it with the CustomUser
    self.tutor_test = CustomUser.objects.create(
        email='sergi@wsu.edu',
        first_name='Sergi',
        last_name='Oliva',
        is_tutor=True,
        is_student=False,
        is_admin=False
    )

    self.T = Tutor(
        user=self.tutor_test,  # Set the user for the Tutor instance
        hours_tutored=0,
        day_started=None,
        rating=0.0,
        description='Legendary bodybuilder and Baki Character'
    )
    self.T.save()

    # Create a Class
    self.M = Major.objects.create(name="Computer Science", abbreviation="CS")
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

    def test_shift(self):
        # Create a Shift instance
        shift = Shift.objects.create(
            tutor=self.tutor,
            day='Monday',
            start_time=time(8, 0),  # 8:00 AM
            end_time=time(9, 0)    # 9:00 AM
        )

        # Check the __str__ method
        expected_str = "Monday from 08:00 AM to 09:00 AM"

        # Make sure to use time objects as setting up with datetime requires extraction of time object before use
        self.assertEqual(str(shift), expected_str)

        # Check the tutor relation
        self.assertEqual(shift.tutor, self.tutor)

        # Test Major
    def test_major(self):
        # Ceate a Major instance for testing
        self.major = Major.objects.create(name="Computer Science", abbreviation="CS")
        
        # Check if the __str__ method returns the expected string
        expected_str = "CS"
        self.assertEqual(str(self.major), expected_str)

# Test manage_user_profile
    def test_manage_user_profile_creation(self):
        # Ensure that the corresponding profile is created for the user
        self.assertTrue(Student.objects.filter(user=self.user).exists())
        self.assertFalse(Tutor.objects.filter(user=self.user).exists())
        self.assertFalse(Admin.objects.filter(user=self.user).exists())

    def test_manage_user_profile_role_change(self):
        # Create a test student
        test_student = CustomUser.objects.create(user = self.user)

        # Change user role to Tutor
        test_student.user.is_tutor = True
        test_student.save()

        # Ensure that the corresponding profile is created for the user and other profiles are deleted
        self.assertTrue(Tutor.objects.filter(user=self.user).exists())
        self.assertFalse(Student.objects.filter(user=self.user).exists())
        self.assertFalse(Admin.objects.filter(user=self.user).exists())

        # Change user role to Admin
        self.user.is_admin = True
        self.user.save()

        # Ensure that the corresponding profile is created for the user and other profiles are deleted
        self.assertTrue(Admin.objects.filter(user=self.user).exists())
        self.assertFalse(Student.objects.filter(user=self.user).exists())
        self.assertFalse(Tutor.objects.filter(user=self.user).exists())