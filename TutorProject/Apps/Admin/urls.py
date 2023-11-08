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
    path('administrator/viewtutors', views.admin_view_tutors,name = 'admin_view_tutors'),
    path('administrator/edittutor/<int:tutor_id>', views.admin_edit_tutor_profile,name = 'admin_edit_tutor_profile'),
    path('administrator/classes_menu', views.classes_menu,name = 'classes_menu'),
    path('administrator/majors_menu', views.majors_menu,name = 'majors_menu'),
    path('administrator/delete_class/<int:class_id>', views.delete_class,name = 'delete_class'),
    path('administrator/delete_major/<int:major_id>', views.delete_major,name = 'delete_major'),
    path('administrator/<int:tutor_id>/shifts', views.admin_view_tutor_shifts,name = 'admin_view_tutor_shifts'),
    path('administrator/<int:tutor_id>/addshift', views.admin_add_tutor_shift,name = 'admin_add_tutor_shift'),
    path('administrator/<int:shift_id>/delete/', views.admin_delete_shift, name='admin_delete_shift'),
]