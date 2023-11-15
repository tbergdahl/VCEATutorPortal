import warnings
import os
from django.test import TestCase, override_settings
from django.urls import reverse
from Apps.TutorApp.models import *  # Import your models from the correct location
from django.db import transaction

warnings.filterwarnings("ignore")

class TestTutor(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Constant test data here
        # update
        pass

    @transaction.atomic
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

        # Create a new Tutor instance for each test
        self.tutor = Tutor(
            user=self.tutor_user,
            minutes_tutored=0,
            day_started=None,
            rating=0.0,
            description='Legendary bodybuilder and actor'
        )
        print(Tutor.objects.all())
        self.tutor.save()
        print(Tutor.objects.all())

    @transaction.atomic
    def tearDown(self):
        # Clean up the created objects
        Tutor.objects.all().delete()
        CustomUser.objects.all().delete()
        

    def test_assignment(self):
        # Test tutor assignment
        self.assertFalse(self.tutor.user.is_student)
        self.assertFalse(self.tutor.user.is_admin)
        self.assertTrue(self.tutor.user.is_tutor)

        # Test tutor information
        self.assertEqual(self.tutor.user.email, 'jay.cutler1@wsu.edu')
        self.assertEqual(self.tutor.user.first_name, 'Jay')
        self.assertEqual(self.tutor.user.last_name, 'Cutler')
        self.assertEqual(self.tutor.minutes_tutored, 0)
        self.assertEqual(self.tutor.day_started, None)
        self.assertEqual(self.tutor.rating, 0.0)
        self.assertEqual(self.tutor.description, 'Legendary bodybuilder and actor')

    def test_rating(self):
        print(Tutor.objects.all())
        # Save the tutor instance to the database
        self.tutor.save()

        # Create feedback instances for testing
        test_feedback = Feedback.objects.create(
            tutor=self.tutor,
            rating=5,
            feedback="Great tutor"
        )
        test_feedback_2 = Feedback.objects.create(
            tutor=self.tutor,
            rating=0,
            feedback="Bad tutor"
        )

        # Compute the tutor's rating
        self.tutor.compute_rating()
        self.assertEqual(self.tutor.rating, 2.5)
