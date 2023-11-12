from django.urls import path
from . import views
from .views import *
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'Tutor'
urlpatterns = [

    path('tutor/', views.tutor_view, name='tutor_view'),
    path('tutor/view_appointments/<int:tutor_id>', views.view_appointments, name='view_appointments'),
    path('tutor/cancel_appointment/<int:appointment_id>', views.cancel_appointment, name='cancel_appointment'),
    path('tutor/end_appointment/<int:appointment_id>', views.appointment_completed, name='appointment_completed'),
    path('tutor/view_feedback/<int:tutor_id>', views.view_feedback, name='view_feedback'),
]
