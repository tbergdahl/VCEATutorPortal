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