from django.urls import path
from . import views
from .views import *
from django.contrib.auth.views import LoginView, LogoutView


app_name = 'Admin'
urlpatterns = [
    path('administrator/', views.admin_view, name='admin_view'),
    path('administrator/createuser', views.admin_create_user, name='admin_create_user'),
    path('administrator/deleteuser/', views.admin_delete_user, name='admin_delete_user'),  
    path('administrator/printreports/', views.admin_view_reports, name='admin_view_reports'),
    path('administrator/createclass', views.admin_create_class, name='admin_create_class'),
    path('administrator/createmajor', views.admin_create_major, name='admin_create_major'),
]