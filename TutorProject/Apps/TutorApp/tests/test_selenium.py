
from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from Apps.TutorApp.models import *
from django.contrib.auth import get_user_model
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

from selenium.common.exceptions import TimeoutException

class AppointmentsLinkNotFoundError(TimeoutException):
    pass
class MySeleniumTests(LiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.selenium = webdriver.Chrome() 

    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super().tearDownClass()

    def test_login(self):

        # Create a student user and student
        user_model = get_user_model()
        student_user = user_model.objects.create_user(
            email='ronnie.coleman@wsu.edu',
            password='MySpineIsntbroken123!',
            is_student=True,
            is_tutor=False,
            is_admin=False
        )
        student = Student(user=student_user)

        # Create a tutor user and tutor
        tutor_user = user_model.objects.create(
            email='jay.cutler1@wsu.edu',
            first_name='Jay',
            last_name='Cutler',
            is_tutor=True,
            is_student=False,
            is_admin=False
        )
        tutor = Tutor(
            user=tutor_user,
            hours_tutored=0,
            day_started=None,
            rating=0.0,
            description='Legendary bodybuilder and actor'
        )

        student.save()
        tutor.save()

        # Open the selenium browser
        self.selenium.get(self.live_server_url)

        # Wait for the email input field to be present
        email_input = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        time.sleep(1) # wait for bettter visibility
        # Continue with your test
        email_input.send_keys("ronnie.coleman@wsu.edu")

        # Similarly, locate the password input field
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("MySpineIsntbroken123!")

        # Click the login button
        login_button = self.selenium.find_element(By.CSS_SELECTOR, ".loginPage-submit-button")
        login_button.click()

        # Wait for the student page to load
        student_page_title = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h2[text()='Rate your Tutors']"))
        )
        time.sleep(1) # wait for bettter visibility


        # Check if the tutor list is present
        tutor_list = self.selenium.find_elements(By.CLASS_NAME, "student-tutor-card")
        self.assertTrue(len(tutor_list) > 0, "Tutor list is empty")

        time.sleep(1) # wait for bettter visibility

        # Click on the first tutor
        first_tutor = tutor_list[0]
        first_tutor.find_element(By.CLASS_NAME, "student-action-button").click()
        
        # After viewing the tutor, navigate to the Appointments section
        time.sleep(1) # wait for bettter visibility

        self.selenium.get(self.live_server_url + "/appointments/1/")  # Update the URL with the correct path

        

        