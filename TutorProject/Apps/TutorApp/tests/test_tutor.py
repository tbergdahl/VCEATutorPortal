import warnings
import os
from django.test import TestCase, override_settings
from django.urls import reverse
from Apps.TutorApp.models import *  # Import your models from the correct location
from django.db import transaction

#Use mysql test db

warnings.filterwarnings("ignore")

class TestTutor(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Constant test data here
        # update
        pass

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
        self.tutor.save()

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

    def test_create_appointments(self):
        # Create a Shift for testing
        test_shift = Shift.objects.create(
            tutor=self.tutor,
            day='Monday',
            start_time=datetime.now().time(),
            end_time=(datetime.now() + timedelta(hours=1)).time()
        )

        # Add the test shift to the tutor's shifts
        self.tutor.shifts.add(test_shift)

        # Set the current_datetime to a specific day and time
        current_datetime = datetime(2023, 1, 1, 12, 0, 0)  # Replace with your desired datetime
        self.tutor.create_appointments()

        # Check that the appointment was created
        shift_datetime = datetime.combine(current_datetime.date(), test_shift.start_time)
        self.assertTrue(Shift.objects.filter(tutor=self.tutor, start_time=shift_datetime).exists())
