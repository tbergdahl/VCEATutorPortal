from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from .forms import *
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import *

# Create your views here.
def student_view(request):
    return render(request, 'studentPage.html')
def tutor_view(request):
    return render(request, 'tutorPage.html')
def admin_view(request):
    return render(request, 'adminPage.html')
def admin_view_createuser(request):
    return render(request, 'createuser.html')
def admin_view_deleteuser(request):
    return render(request, 'deleteUser.html')




def home(request):
    if request.user.is_authenticated:
        if request.user.is_admin:
            return redirect(reverse('Admin:admin_view'))
        elif request.user.is_student:
            return redirect(reverse('Student:student_view'))
        elif request.user.is_tutor:
            return redirect(reverse('Tutor:tutor_view'))
    
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if user.is_admin:
                return redirect(reverse('Admin:admin_view'))
            elif user.is_student:
                return redirect(reverse('Student:student_view'))
            elif user.is_tutor:
                return redirect(reverse('Tutor:tutor_view'))
        else:
            messages.error(request, 'Invalid email or password.')

    else:
        form = AuthenticationForm()

    return render(request, "login.html", {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Log the user in.
            login(request, user)
            
            return redirect(reverse('Student:student_view'))  # Use the name of the URL pattern
    else:
        form = CustomUserCreationForm()

    return render(request, 'register.html', {'form': form})












# update


