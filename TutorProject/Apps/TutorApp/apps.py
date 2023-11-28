from django.apps import AppConfig
from django.db.models.signals import post_migrate
from datetime import timezone, timedelta


class TutorAppConfig(AppConfig):
    name = 'Apps.TutorApp'
    def ready(self):
        from background_task.models import Task
        from Apps.TutorApp.tasks import my_scheduled_task
        my_scheduled_task(schedule=timedelta(hours=11, minutes=7),repeat=Task.DAILY, repeat_until=None)

class TutorappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TutorApp'
    
    