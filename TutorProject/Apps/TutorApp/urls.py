from django.urls import path
from . import views
from .views import *
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register, name="register"),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('password_reset_request/', views.password_reset_combined, name='password_reset_request'),
    path('password_reset/<int:user_id>/', views.password_reset, name='password_reset'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)