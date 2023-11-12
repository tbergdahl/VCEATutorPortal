from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from .forms import *
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from django.core.mail import send_mail
from .models import PasswordResetCode, CustomUser
from .forms import PasswordResetRequestForm
from .forms import PasswordResetForm
from django.contrib.auth.hashers import make_password

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

def password_reset_combined(request):
    request_form = PasswordResetRequestForm(request.POST or None, prefix="request")
    verify_form = PasswordResetVerificationForm(request.POST or None, prefix="verify")

    if 'request' in request.POST and request_form.is_valid():
        email = request_form.cleaned_data['email']
        try:
            user = CustomUser.objects.get(email=email)
            reset_code, created = PasswordResetCode.objects.get_or_create(user=user)
            send_mail(
                'Your Password Reset Code',
                f'Your password reset code is: {reset_code.code}',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
            messages.success(request, "Password reset code sent successfully.")
        except CustomUser.DoesNotExist:
            messages.error(request, "Email address not found.")

    elif 'verify' in request.POST and verify_form.is_valid():
        code = verify_form.cleaned_data['code']
        try:
            reset_code = PasswordResetCode.objects.get(code=code)
            return redirect('password_reset', user_id=reset_code.user.id)
        except PasswordResetCode.DoesNotExist:
            messages.error(request, "The reset code entered is incorrect or expired. Please try again.")

    context = {
        'request_form': request_form,
        'verify_form': verify_form,
    }
    return render(request, 'password_reset_request.html', context)



def password_reset(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    form = PasswordResetForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        new_password = form.cleaned_data['new_password']

        user.set_password(new_password)
        user.save()
        messages.success(request, "Your password has been reset successfully.")
        return redirect('login')  # Redirect to login page after reset

    return render(request, 'password_reset.html', {'form': form})









# update


