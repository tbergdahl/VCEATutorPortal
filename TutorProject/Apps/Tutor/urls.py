from django.urls import path
from . import views
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [

    path('tutor/', views.tutor_view, name='tutor_view'),

]