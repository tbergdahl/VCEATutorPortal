from django.urls import path
from . import views
from .views import *
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'Admin'
urlpatterns = [
    path('administrator/', views.admin_view, name='admin_view'),
    path('administrator/createuser', views.admin_create_user, name='admin_create_user'),
    path('administrator/deleteuser/', views.admin_delete_user, name='admin_delete_user'),  
]