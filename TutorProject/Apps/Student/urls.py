from django.urls import path
from . import views
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'Student'
urlpatterns = [

    path('student/', views.student_view, name='student_view'),
    path('rate_tutor/<int:tutor_id>/', rate_tutor, name='rate_tutor'),
    path('view_tutors/<int:tutor_id>/', views.student_view_tutors, name='student_view_tutors'),
    path('book_appointment/<int:appointment_id>/', views.book_appointment, name='book_appointment'),
    path('appointments/<int:student_id>/', views.student_view_appointments, name='student_view_appointments'),
    path('student/cancel_appointment/<int:appointment_id>', views.cancel_appointment, name='cancel_appointment'),
]