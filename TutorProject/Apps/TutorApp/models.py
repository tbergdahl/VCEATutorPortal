from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.contrib.auth.models import BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime, timedelta
from django.db.models import Q
import uuid
import random
import string

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(("email address"), unique = True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    first_name = models.CharField(max_length=30, blank=False)  
    last_name = models.CharField(max_length=30, blank=False)  
    is_admin = models.BooleanField(default=False)
    is_student = models.BooleanField(default=True)
    is_tutor = models.BooleanField(default=False)
    objects = CustomUserManager()


class Major(models.Model):
    name = models.CharField(max_length=100)
    abbreviation = models.CharField(max_length=20, default="placeholder")

    def __str__(self):
        return self.abbreviation





class Admin(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    
class Tutor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    minutes_tutored = models.IntegerField(default=0)
    day_started = models.DateField(max_length=20, null=True)
    rating = models.FloatField(default=0, validators=[MaxValueValidator(5.0), MinValueValidator(0.0)])
    description = models.TextField(blank=True, null=True)
    major = models.ForeignKey(Major, on_delete=models.CASCADE, null=True)
    token = models.CharField(max_length=50, null=True, blank=True)
    picture = models.ImageField(upload_to='tutor_pictures/', null=True, blank=True)

    def compute_rating(self):
        rating = 0
        count = 0
        for feedback in self.feedback.all():
            rating += feedback.rating
            count += 1           
        self.rating = rating / count
        self.save()

    def create_appointments(self):
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        current_datetime = datetime.now()
        for shift in self.shifts.all():
            shifts_for_day = Shift.objects.filter(tutor=self, day=shift.day) # get all shifts within a day
            shift_date = self.next_instance_of_shift(shift.day, current_datetime, days) # get date of all the shifts occurrence
            for daily_shift in shifts_for_day: # split into appointments and update the date of the appointment
                self.create_appointments_in_day(shift_date, daily_shift)

    def next_instance_of_shift(self, target_day_name, current_day, days): # finds the date a shift will occur given the name of the day (ex. Monday)
        current_day_index = current_day.weekday() # returns 0 for monday, etc (datetime method)
        
        target_day_index = days.index(target_day_name) # days list is user defined list that starts monday at 0, so if target was Thursday, would be 3
        time_between_current_day_and_target_day = (target_day_index - current_day_index + 7) % 7 # find how many days in between target and current day
        target_shift_next_date = current_day + timedelta(days=time_between_current_day_and_target_day) # use that to get the date of the appointment
        return target_shift_next_date


    def create_appointments_in_day(self, shift_date, shift):
        start_time = datetime.combine(shift_date, shift.start_time)
        end_time = datetime.combine(shift_date, shift.end_time)
        appointment_len = timedelta(minutes=20)
        current_time = start_time

        # Check if there are any existing appointments on the specified day
        existing_appointments_on_day = TutoringSession.objects.filter(
            tutor=self,
            start_time__date=shift_date.date()
        ).exists()

        if not existing_appointments_on_day:
            while current_time < end_time:
                app_end_time = current_time + appointment_len

                # Create a new appointment
                appointment = TutoringSession(start_time=current_time, end_time=app_end_time)
                appointment.tutor = self
                appointment.save()
                self.appointments.add(appointment)
                shift.appointments.add(appointment)
                print(f"Added Appointment at {current_time} to tutor's appointments.")

                current_time += appointment_len
        else:
            print(f"Appointments already exist on {shift_date}. Skipping generation.")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

def generate_reset_codes():
    return ''.join(random.choices(string.digits, k=6))

class PasswordResetCode(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, default=generate_reset_codes)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Password reset code for {self.user.email}"

class Feedback(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='feedback')
    feedback = models.CharField(max_length=500, null=True)
    rating = models.FloatField(blank=True)

class Student(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
    
#connect the relationship to the student, tutor, and admin
@receiver(post_save, sender=CustomUser)
def manage_user_profile(sender, instance, created, **kwargs):
    # Handle new user creation
    if created:
        if instance.is_student:
            Student.objects.create(user=instance)
        elif instance.is_admin:
            Admin.objects.create(user=instance)
        elif instance.is_tutor:
            Tutor.objects.create(user=instance)
        return

    # Handle role changes for existing users
    if instance.is_student:
        Student.objects.get_or_create(user=instance)
        Admin.objects.filter(user=instance).delete()
        Tutor.objects.filter(user=instance).delete()
    elif instance.is_admin:
        Admin.objects.get_or_create(user=instance)
        Student.objects.filter(user=instance).delete()
        Tutor.objects.filter(user=instance).delete()
    elif instance.is_tutor:
        Tutor.objects.get_or_create(user=instance)
        Student.objects.filter(user=instance).delete()
        Admin.objects.filter(user=instance).delete()


class Class(models.Model):
    class_major = models.ForeignKey(Major, on_delete=models.CASCADE)
    course_num = models.IntegerField()
    course_name = models.CharField(max_length=100, null=True)
    available_tutors = models.ManyToManyField(Tutor, related_name="tutored_classes")
    hours_tutored = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.class_major.abbreviation} {self.course_num}"





class Shift(models.Model):
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='shifts')
    day = models.CharField(max_length=20)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.day} from {self.start_time.strftime('%I:%M %p')} to {self.end_time.strftime('%I:%M %p')}"
    
class TutoringSession(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='appointments', null=True, blank=True)
    tutor = models.ForeignKey(Tutor, on_delete=models.CASCADE, related_name='appointments')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    tutored_class = models.ForeignKey(Class, on_delete=models.CASCADE, null=True)
    description = models.CharField(max_length=300, null=True)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name='appointments', null=True)

    def __str__(self):
        return f"Appointment with {self.tutor} from {self.start_time.strftime('%I:%M %p')} to {self.end_time.strftime('%I:%M %p')}"