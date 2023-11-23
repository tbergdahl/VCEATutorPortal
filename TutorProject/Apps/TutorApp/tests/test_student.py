import warnings
import os
from django.test import TestCase, override_settings
from django.urls import reverse
from Apps.TutorApp.models import *  # Import your models from the correct location

warnings.filterwarnings("ignore")

class TestStudent(TestCase):
    def setUp(self):
        self.student_user = CustomUser.objects.create(
            email='ronnie.coleman@wsu.edu',
            first_name='Ronnie',
            last_name='Coleman',
            is_student=True,
            is_tutor=False,
            is_admin=False
        )
        self.student = Student(user=self.student_user)
        self.student.save()

    def tearDown(self):
        # Delete the created objects to clean up
        CustomUser.objects.all().delete()
        Student.objects.all().delete()
    
    def test_Student_Assignment(self):
        # Test student assignment
        self.assertTrue(self.student.user.is_student)
        self.assertFalse(self.student.user.is_tutor)
        self.assertFalse(self.student.user.is_admin)

        # Test one to one field relationship (with assignments)
        self.assertTrue(self.student.user.email, 'ronnie.coleman@wsu.edu')
        self.assertTrue(self.student.user.first_name, 'Ronnie')
        self.assertTrue(self.student.user.last_name, 'Coleman')
        
        # Test string def method
        expected_string = "Ronnie Coleman"
        self.assertEqual(str(self.student), expected_string)