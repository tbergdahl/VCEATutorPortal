
from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from Apps.TutorApp.models import *
from django.contrib.auth import get_user_model
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        # Create a student user
        user_model = get_user_model()
        student_user = user_model.objects.create_user(
            email='ronnie.coleman@wsu.edu',
            password='MySpineIsntbroken123!',
            is_student=True,
            is_tutor=False,
            is_admin=False
        )
        student = Student(user=student_user)
        student.save()

        # Open the selenium browser
        self.selenium.get(self.live_server_url)

        # Wait for the email input field to be present
        email_input = WebDriverWait(self.selenium, 10).until(
            EC.presence_of_element_located((By.NAME, "username"))
        )

        # Continue with your test
        email_input.send_keys("ronnie.coleman@wsu.edu")

        # Similarly, locate the password input field
        password_input = self.selenium.find_element(By.NAME, "password")
        password_input.send_keys("MySpineIsntbroken123!")

        # Click the login button
        login_button = self.selenium.find_element(By.CSS_SELECTOR, ".loginPage-submit-button")
        login_button.click()
        