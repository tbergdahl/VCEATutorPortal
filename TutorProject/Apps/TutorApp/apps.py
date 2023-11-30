from django.apps import AppConfig
from django.db.models.signals import post_migrate
from datetime import timezone, timedelta


class TutorAppConfig(AppConfig):
    name = 'Apps.TutorApp'
    def ready(self):
        from background_task.models import Task
        from Apps.TutorApp.tasks import my_scheduled_task
        my_scheduled_task(schedule=timedelta(hours=11, minutes=7),repeat=Task.DAILY, repeat_until=None)
        self.create_time_slots(self)
        pass

    @staticmethod
    def create_time_slots(self):
        from .models import TimeSlot, TutoringTimePeriod
        from datetime import time, timedelta, datetime

        start_time = time(7, 0)  
        end_time = time(21, 0)
        interval_minutes = 20

        current_time = start_time
        while current_time < end_time:
            try:
               TimeSlot.objects.get(start_time=current_time)
            except TimeSlot.DoesNotExist:
                TimeSlot.objects.create(start_time=current_time)
            current_time = (datetime.combine(datetime.today(), current_time) + timedelta(minutes=interval_minutes)).time()

        start_time = time(7, 0)  
        end_time = time(21, 0)
        interval_minutes = 60

        current_time = start_time
        while current_time < end_time:
            try:
                TutoringTimePeriod.objects.get(start_time=current_time)
            except TutoringTimePeriod.DoesNotExist:
                TutoringTimePeriod.objects.create(start_time=current_time)
            current_time = (datetime.combine(datetime.today(), current_time) + timedelta(minutes=interval_minutes)).time()
        

class TutorappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TutorApp'
    
    