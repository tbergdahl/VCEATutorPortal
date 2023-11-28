from django.apps import AppConfig



class TutorAppConfig(AppConfig):
    name = 'Apps.TutorApp'
class TutorappConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'TutorApp'
    
    def ready(self):
        from . import tasks
        tasks.my_scheduled_task()