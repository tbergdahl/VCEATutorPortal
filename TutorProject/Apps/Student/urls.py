from django.urls import path
from . import views
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [

    path('student/', views.student_view, name='student_view'),

]