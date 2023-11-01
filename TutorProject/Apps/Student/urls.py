from django.urls import path
from . import views
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

app_name = 'Student'
urlpatterns = [

    path('student/', views.student_view, name='student_view'),
    path('rate_tutor/<int:tutor_id>/', rate_tutor, name='rate_tutor'),

]