import warnings
import os
from django.test import TestCase, override_settings
from django.urls import reverse
from Apps.TutorApp.models import *  # Import your models from the correct location

warnings.filterwarnings("ignore")

class TestTutor(TestCase):
    def setUp(self):
        # Create a test user
        self.tutor_user = CustomUser.objects.create(
            email='jay.cutler1@wsu.edu',
            first_name='Jay',
            last_name='Cutler',
            is_tutor=True,
            is_student=False,
            is_admin=False
        )
        self.tutor_user.save()

        self.Tutor = Tutor(
            user=self.tutor_user,
            minutes_tutored=0,
            day_started=None,
            rating=0.0,
            description='Legendary bodybuilder and actor'
        )
        self.Tutor.save()

    def tearDown(self):
        # Delete the created objects to clean up
        CustomUser.objects.all().delete()
        Tutor.objects.all().delete()


    def test_assignment(self):
        # Test tutor assignment
        self.assertFalse(self.Tutor.user.is_student)
        self.assertFalse(self.Tutor.user.is_admin)
        self.assertTrue(self.Tutor.user.is_tutor)

        # Test tutor information
        self.assertEqual(self.Tutor.user.email, 'jay.cutler1@wsu.edu')
        self.assertEqual(self.Tutor.user.first_name, 'Jay')
        self.assertEqual(self.Tutor.user.last_name, 'Cutler')
        self.assertEqual(self.Tutor.minutes_tutored, 0)
        self.assertEqual(self.Tutor.day_started, None)
        self.assertEqual(self.Tutor.rating, 0.0)
        self.assertEqual(self.Tutor.description, 'Legendary bodybuilder and actor')

    def test_rating(self):
        test_feedback = Feedback(
            tutor=self.Tutor,
            rating=5,
            feedback="Great tutor"
        )
        test_feedback_2 = Feedback(
            tutor=self.Tutor,
            rating=0,
            feedback="Bad tutor"
        )

        test_feedback.save()
        test_feedback_2.save()

        self.Tutor.compute_rating()
        self.assertEqual(self.Tutor.rating, 2.5)


