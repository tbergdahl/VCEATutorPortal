# Create your tests here.
from django.test import TestCase, Client
from django.urls import reverse
from Apps.TutorApp.models import *
from Apps.TutorApp.forms import *
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
import warnings
from django.utils import timezone, dateformat
from datetime import datetime, time
from django.core.exceptions import ValidationError

warnings.filterwarnings("ignore")

class TutorViewsTest(TestCase):
    def setup(self):
        pass