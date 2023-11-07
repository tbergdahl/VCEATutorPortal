from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, authenticate
from Apps.TutorApp.forms import *
from django.urls import reverse_lazy
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from Apps.TutorApp.models import *
from Apps.TutorApp.forms import *
from io import BytesIO
# views.py
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table
from django.shortcuts import get_object_or_404


def admin_view(request):
    return render(request, 'adminPage.html')

def admin_create_user(request):
    if not request.user.is_admin:
        return redirect('home')

    if request.method == 'POST':
        form = AdminCreateUser(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Don't save yet
            role = form.cleaned_data.get('role')
            if role == 'is_student':
                user.is_student = True
                user.save()
                Student.objects.create(user=user)
            elif role == 'is_tutor':
                user.is_tutor = True
                user.save()
                Tutor.objects.create(user=user)
            elif role == 'is_admin':
                user.is_admin = True
                user.save()
                Admin.objects.create(user=user)
            
        return redirect('Admin:admin_view')
    else:
        form = AdminCreateUser()

    return render(request, 'createuser.html', {'form': form})


def admin_delete_user(request):
    
    if not request.user.is_admin:
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('home')

   
    users = CustomUser.objects.filter(is_admin=False)

    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')  
        try:
            user_to_delete = CustomUser.objects.get(pk=user_id)
            if user_to_delete.is_admin:
                messages.error(request, 'Cannot delete another admin.')
            else:
                user_to_delete.delete()
                messages.success(request, 'User deleted successfully.')
        except ObjectDoesNotExist:
            messages.error(request, 'User not found.')


    role = request.GET.get('role', '')
    if role == 'student':
        users = users.filter(is_student=True)
    elif role == 'tutor':
        users = users.filter(is_tutor=True)

    search_query = request.GET.get('search', '')
    if search_query:
        users = users.filter(email__icontains=search_query)

    return render(request, 'deleteUser.html', {'users': users})

    
def admin_view_reports(request):
    if request.method == 'POST':
        form = PDFSelectionForm(request.POST)
        if form.is_valid():
            report = form.cleaned_data['report']
            response = HttpResponse(content_type='application/pdf')
            
            if report == 'report1':
                response['Content-Disposition'] = 'attachment; filename="Tutor Statistics Report.pdf"'
                response.write(report1().getvalue())
                
            elif report == 'report2':
                response['Content-Disposition'] = 'attachment; filename="Hours By Class.pdf"'
                response.write(report2().getvalue())

            elif report == 'report3':
                response['Content-Disposition'] = 'attachment; filename="generated_pdf.pdf"'
                response.write(report3().getvalue())
            else:
                response.write("No Report Available")

            return response
            
    else:
        form = PDFSelectionForm()

    return render(request, 'generate_pdf.html', {'form': form})

def admin_view_tutors(request):
    tutors = Tutor.objects.all()
    return render(request, 'tutors.html', {'tutors': tutors})

def admin_edit_tutor_profile(request, tutor_id):
    tutor = get_object_or_404(Tutor, id=tutor_id)
    if request.method == 'POST':
        form = EditTutorForm(request.POST, instance=tutor)
        if form.is_valid():
            user_instance = tutor.user  
            user_instance.first_name = form.cleaned_data['first_name']
            user_instance.last_name = form.cleaned_data['last_name']
            user_instance.save()
            form.save()  

            selected_major = form.cleaned_data.get('major')
            user_instance.major = selected_major
            user_instance.save()

            selected_classes = form.cleaned_data.get('tutored_classes')
            for a_class in selected_classes:
                a_class.available_tutors.add(tutor)
            
    else:
        associated_classes = tutor.tutored_classes.all()
        form = EditTutorForm(instance=tutor, initial={'tutored_classes': associated_classes})
    
    return render(request, 'edit_tutor.html', {'form': form})

def report1():
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    tutors = Tutor.objects.all()
    data = [['Tutor', 'Minutes Tutored', 'Rating'],]

    for tutor in tutors:
        data.append([f"{tutor.user.first_name} {tutor.user.last_name}", tutor.minutes_tutored, tutor.rating])

    table = Table(data)
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige)
    ]

    table.setStyle(style)
    elements = [table]
    pdf.build(elements)

    buffer.seek(0)
    return buffer

def report2():
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    classes = Class.objects.all().order_by('hours_tutored')

    totalHours = 0
    for aclass in classes:
        totalHours += aclass.hours_tutored

    

    data = [['Total Hours Tutored', totalHours],['Hours By Class']]

    for aclass in classes:
        data.append([f"{aclass.class_major.name} - {aclass.course_num} - {aclass.course_name}", f"Hours: {aclass.hours_tutored}" ])

    table = Table(data)
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige)
    ]

    table.setStyle(style)
    elements = [table]
    pdf.build(elements)

    buffer.seek(0)
    return buffer 


def report3():
    pass

def classes_menu(request):
    classes = Class.objects.all()
    return render(request, 'classes.html', {'classes': classes})

def majors_menu(request):
    majors = Major.objects.all()
    return render(request, 'majors.html', {'majors': majors})


def admin_create_class(request):
    if request.method == 'POST':
        form = ClassCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Admin:admin_view')  
    else:
        form = ClassCreationForm()
    return render(request, 'create_class.html', {'form': form})



def admin_create_major(request):
    if request.method == 'POST':
        form = MajorCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Admin:admin_view')
    else:
        form = MajorCreationForm()

    return render(request, 'create_major.html', {'form': form}) 


def delete_class(request, class_id):
    a_class = get_object_or_404(Class, pk=class_id)
    a_class.delete()
    return redirect('Admin:classes_menu')

def delete_major(request, major_id):
    a_major = get_object_or_404(Major, pk=major_id)
    a_major.delete()
    return redirect('Admin:majors_menu')