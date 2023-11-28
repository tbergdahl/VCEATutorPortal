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
            from .models import TimeSlot
            from datetime import time, timedelta, datetime

            start_time = datetime.combine(datetime.today(), datetime.min.time()) + timedelta(hours=7)
            end_time = datetime.combine(datetime.today(), datetime.min.time()) + timedelta(hours=21)
            interval_minutes = 20
            current_time = start_time
            while current_time < end_time:
                print(f"Created Time Slot For {current_time}")
                TimeSlot.objects.get_or_create(start_time=current_time)
                current_time += timedelta(minutes=interval_minutes)

class TutorappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TutorApp'
    
    