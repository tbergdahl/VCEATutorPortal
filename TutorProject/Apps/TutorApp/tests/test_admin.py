import warnings
import os
from django.test import TestCase, override_settings
from django.urls import reverse
from Apps.TutorApp.models import *  # Import your models from the correct location

warnings.filterwarnings("ignore")

class TestAdmin(TestCase):
    def setUp(self):
        # Create a test user for each role
        self.admin_user = CustomUser.objects.create(
            email='phil.health@wsu.edu',
            first_name='Phil',
            last_name='Heath',
            is_admin=True,
            is_student=False,
            is_tutor=False
        )
        self.admin = Admin(user=self.admin_user)
        self.admin.save()
    
    def tearDown(self):
        # Delete the created objects to clean up
        CustomUser.objects.all().delete()
        Admin.objects.all().delete()

    def test_Admin_Assignment(self):
        # Test admin assignment
        self.assertTrue(self.admin.user.is_admin)
        self.assertFalse(self.admin.user.is_student)
        self.assertFalse(self.admin.user.is_tutor)

        # Test admin information
        self.assertEqual(self.admin.user.email, 'phil.health@wsu.edu')
        self.assertEqual(self.admin.user.first_name, 'Phil')
        self.assertEqual(self.admin.user.last_name, 'Heath')