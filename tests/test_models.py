import pytest
import unittest
import warnings
import os
from django.test import TestCase, Client, reverse
from TutorProject.Apps.TutorApp.models import *  #import CustomUser from TutorApp.models
warnings.filterwarnings("ignore")

basedir = os.path.abspath(os.path.dirname(__file__))



class TestConfig(TestCase):
    TESTING = True
    ROOT_PATH = '..//'+ basedir
    #enter the database link

class TestModels(unittest.TestCase):
    def setUp(self): # creates all model instances

        # create tutor
        self.t = Tutor(username='Jay', 
                  email = 'jay.cutler@wsu.edu',
                  is_student=False, is_tutor=True, is_admin=False)
        self.t.set_password('test_password')
        self.t.save()

        # create admin
        self.a = Admin(username='Arnold', 
                  email = 'arnold.schwarzenegger@wsu.edu',
                  is_student=False, is_tutor=False, is_admin=True)
        self.a.set_password('test_password')
        self.a.save()

        # create student
        self.s = Student(username='Ronnie', 
                    email = 'ronnie.coleman@wsu.edu',
                    is_student=True, is_tutor=False, is_admin=False)
        self.s.set_password('test_password')
        self.s.save()

    def tearDown(self):  # deletes all model instances
        #delete tutor
        self.t.delete()

        #delete admin
        self.a.delete()

        #delete student
        self.s.delete()

    def test_password_hashing(self): # test that the password hashing is behaving as expected
        u = CustomUser(username='Ronnie', email='ronnie.coleman@wsu.edu')
        u.set_password('testing123')
        self.assertFalse(u.get_password('testing234'))
        self.assertTrue(u.get_password('testing123'))
        

    def test_all_uers(self):  #tests that you can create and delete all user types
        # create tutor
        t = Tutor(username='Jay1', 
                  email = 'jay.cutler1@wsu.edu',
                  is_student=False, is_tutor=True, is_admin=False)
        t.save()
        # create admin
        a = Admin(username='Arnold1', 
                  email = 'arnold1.schwarzenegger@wsu.edu',
                  is_student=False, is_tutor=False, is_admin=True)
        a.save()
        # create student
        s = Student(username='Ronnie1', 
                    email = 'ronnie1.coleman@wsu.edu',
                    is_student=True, is_tutor=False, is_admin=False)
        s.save()

        #delete tutor
        t.delete()
        #delete admin
        a.delete()
        #delete student
        s.delete()

    def verification_testing(self):

        self.client = Client() # create test client

        # Test student login and logout
        self.client.login(username='Ronnie', password='test_password')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

        # Test Admin login and Logout
        self.client.login(username='Arnold', password='test_password')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

        # Test Tutor login and Logout
        self.client.login(username='Jay', password='test_password')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)


    def test_appointment_deletion(self):
        pass

    def test_appointment_update(self):
        pass

if __name__ == '__main__':
    unittest.main(verbosity=2)