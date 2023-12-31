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
from django.db import IntegrityError
from django.utils import timezone
from django.http import HttpResponse
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import uuid
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.core.mail import send_mail

@login_required
def admin_view(request):
    if not request.user.is_admin:
        return HttpResponseForbidden("You do not have permission to view this page.")
    return render(request, 'adminPage.html')


# In your views.py


@login_required
def admin_create_user(request):
    if not request.user.is_admin:
        return redirect('home')

    if request.method == 'POST':
        form = AdminCreateUser(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            role = form.cleaned_data.get('role', 'is_student')
            
            if role == 'is_student':
                user.is_student = True
                user.is_admin = False
                user.is_tutor = False
            elif role == 'is_tutor':
                user.is_tutor = True
                user.is_student = False
                user.is_admin = False
            elif role == 'is_admin':
                user.is_admin = True
                user.is_student = False
                user.is_tutor = False
                
                
            try:
                user.save()
                if role == 'is_student' and not Student.objects.filter(user=user).exists():
                    Student.objects.create(user=user)
                elif role == 'is_tutor' and not Tutor.objects.filter(user=user).exists():
                    token = str(uuid.uuid4())[:8]
                    Tutor.objects.create(user=user, token=token)
                elif role == 'is_admin' and not Admin.objects.filter(user=user).exists():
                    Admin.objects.create(user=user)
            except IntegrityError as e:
                
                messages.error(request, 'A user with this ID already exists.')
                return redirect('Admin:admin_view')
            
            return redirect('Admin:admin_view')
    else:
        form = AdminCreateUser()

    return render(request, 'createuser.html', {'form': form})


@login_required
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

@login_required
def admin_view_reports(request):
    # Handle AJAX request for PDF preview
    if request.method == 'GET' and request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        report_type = request.GET.get('report_type')

        pdf_data = generate_pdf_data(report_type)
        if pdf_data:
            return HttpResponse(pdf_data, content_type='application/pdf')
        else:
            return JsonResponse({'error': 'No PDF data'}, status=500)

    # Handle form submission for PDF download
    elif request.method == 'POST':
        form = PDFSelectionForm(request.POST)
        if form.is_valid():
            report_type = form.cleaned_data['report']
            pdf_data = generate_pdf_data(report_type)
            if pdf_data:
                response = HttpResponse(pdf_data, content_type='application/pdf')
                response['Content-Disposition'] = f'attachment; filename="{report_type}.pdf"'
                return response
            else:
                return HttpResponse("No Report Available")

    # GET request handling for initial form rendering
    else:
        form = PDFSelectionForm()
        return render(request, 'generate_pdf.html', {'form': form})
@login_required
# Utility function to generate PDF data based on report type
def generate_pdf_data(report_type):
    if report_type == 'report1':
        return report1().getvalue()
    elif report_type == 'report2':
        return report2().getvalue()
    elif report_type == 'report3':
        return report3().getvalue()
    elif report_type == 'report4':
        return report4().getvalue()
    elif report_type == 'report5':
        return report4().getvalue()
    else:
        return None
    
@login_required
def pdf_preview(request):
    report_type = request.GET.get('report_type')

    if report_type not in ['report1', 'report2', 'report3', 'report4', 'report5']:
        return HttpResponse("Invalid report type", status=400)

    if report_type == 'report1':
        pdf_data = report1().getvalue()
    elif report_type == 'report2':
        pdf_data = report2().getvalue()
    elif report_type == 'report3':
        pdf_data = report3().getvalue()
    elif report_type == 'report4':
        pdf_data = report4().getvalue()
    elif report_type == 'report5':
        pdf_data = report5().getvalue()
    else:
        return HttpResponse("Invalid report type", status=400)

    if pdf_data:
        response = HttpResponse(pdf_data, content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="preview.pdf"'
        return response
    else:
        return HttpResponse("No PDF data", status=500)

@login_required
def admin_view_tutors(request):
    tutors = Tutor.objects.all()
    return render(request, 'tutors.html', {'tutors': tutors})
@login_required
def admin_edit_tutor_profile(request, tutor_id):
    tutor = get_object_or_404(Tutor, user_id=tutor_id)
    print(tutor) # delete after debug
    if request.method == 'POST':
        print(tutor) # delete after debug
        form = EditTutorForm(request.POST, instance=tutor)
        if form.is_valid():
            print(tutor) # delete after debug
            form.save()  
            if 'picture' in request.FILES:
                tutor.picture = request.FILES['picture']
                tutor.save()
            selected_major = form.cleaned_data.get('major')
            tutor.major = selected_major
            # update name
            new_first_name = form.cleaned_data.get('first_name') # Grab new first name
            tutor.user.first_name = new_first_name # update tutor first name
            new_last_name = form.cleaned_data.get('last_name') # Grab new last name
            tutor.user.last_name = new_last_name # update tutor last name
            tutor.user.save() # Save info

            selected_classes = form.cleaned_data.get('tutored_classes')
            for a_class in selected_classes:
                a_class.available_tutors.add(tutor)
    
    else:
        associated_classes = tutor.tutored_classes.all()
        form = EditTutorForm(instance=tutor, initial={'tutored_classes': associated_classes})

        
    
    return render(request, 'edit_tutor.html', {
        'tutor_form': form,
    })

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
def report1():
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    
    styles = getSampleStyleSheet()

    # Add a debugging line
    
    
    tutors = Tutor.objects.all()
    data = [['Tutor', 'Hours Tutored', 'Rating'],]

    for tutor in tutors:
        data.append([f"{tutor.user.first_name} {tutor.user.last_name}", tutor.hours_tutored, tutor.rating])

    table = Table(data)
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white)
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
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    total_returning_students = Student.objects.filter(times_visited__gt=1)
    total_returning_students_count = Student.objects.filter(times_visited__gt=1).count()
    total_students_count = Student.objects.count()
    percentage = total_returning_students_count / total_students_count
    data = [["Percentage of Returning Students", f"{percentage:.2f}%"], ["Returning Students - Number of Visits"]]

    for student in total_returning_students:
        data.append([f"{student.user.first_name} {student.user.last_name} - {student.times_visited}" ])

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

def report4():
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    data = [["Times Tutoring Center Most Visited"]]

    times = TimeSlot.objects.order_by('-frequency')
    for time_slot in times:
        data.append([f"{time_slot.start_time} - {time_slot.frequency}"])
    

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


def report5():
    from collections import defaultdict
    buffer = BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)
    data = [["Active Tutoring Hours By Tutor"]]

    tutor_frequency_pairs = TutorFrequencyPair.objects.order_by('-frequency')

    tutor_time_slots = defaultdict(list)

    for pair in tutor_frequency_pairs:
        tutor_name = pair.tutor.user.first_name 
        time_slot = pair.time_period.start_time
        frequency = pair.frequency

        # Store time slots for each tutor
        tutor_time_slots[tutor_name].append((time_slot, frequency))

    # Reformat the data to display each tutor's most frequent time slots
    

    for tutor, time_slots in tutor_time_slots.items():
        # Sort the time slots by frequency in descending order
        sorted_time_slots = sorted(time_slots, key=lambda x: x[1], reverse=True)

        # Add tutor's name as a header
        data.append([f"Tutor: {tutor}"])
        
        # Add sorted time slots for this tutor
        for time_slot, frequency in sorted_time_slots:
            data.append([f"Hour: {time_slot}", f"Time Tutored: {frequency}"])

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

@login_required
def classes_menu(request):
    classes = Class.objects.all()
    return render(request, 'classes.html', {'classes': classes})
@login_required
def majors_menu(request):
    majors = Major.objects.all()
    return render(request, 'majors.html', {'majors': majors})

@login_required
def admin_create_class(request):
    if request.method == 'POST':
        form = ClassCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Admin:admin_view')  
    else:
        form = ClassCreationForm()
    return render(request, 'create_class.html', {'form': form})


@login_required
def admin_create_major(request):
    if request.method == 'POST':
        form = MajorCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Admin:admin_view')
    else:
        form = MajorCreationForm()

    return render(request, 'create_major.html', {'form': form}) 

@login_required
def delete_class(request, class_id):
    a_class = get_object_or_404(Class, pk=class_id)
    a_class.delete()
    return redirect('Admin:classes_menu')
@login_required
def delete_major(request, major_id):
    a_major = get_object_or_404(Major, pk=major_id)
    a_major.delete()
    return redirect('Admin:majors_menu')
@login_required
def admin_view_tutor_shifts(request, tutor_id):
   tutor = get_object_or_404(Tutor, user_id=tutor_id)
   shifts = Shift.objects.filter(tutor=tutor)
   form = ShiftForm()
   return render(request, 'shifts.html', {'tutor': tutor, 'shifts': shifts, 'form': form})
from Apps.TutorApp.tasks import my_scheduled_task

@login_required
def admin_add_tutor_shift(request, tutor_id):
    tutor = get_object_or_404(Tutor, user_id=tutor_id) #get tutor info
    form = None
    if request.method == 'POST':
        form = ShiftForm(request.POST)
        if form.is_valid():
            shift = form.save(commit = False)
            shift.tutor = tutor #add tutor to shift
            shift.save()
            tutor.create_appointments()
            return redirect('Admin:admin_view_tutor_shifts', tutor_id = tutor.user_id) #refresh
    else:
        form = ShiftForm()
    return render(request, 'add_shift.html', {'form': form, 'tutor': tutor})

@login_required
def admin_delete_shift(request, shift_id):
    shift = get_object_or_404(Shift, id=shift_id)
    tutor_id = shift.tutor.user_id  # save tutor id for refresh
    shift.appointments.all().delete()
    shift.delete()
    return redirect('Admin:admin_view_tutor_shifts', tutor_id=tutor_id)

@login_required
def admin_tutor_called_out(request, tutor_id):
    tutor = get_object_or_404(Tutor, user_id=tutor_id)
    current_date = timezone.now().date()

    start_of_day = datetime.combine(current_date, datetime.min.time(), tzinfo=timezone.get_current_timezone())
    end_of_day = datetime.combine(current_date, datetime.max.time(), tzinfo=timezone.get_current_timezone())

    tutor_appointments = TutoringSession.objects.filter(
        tutor=tutor,
        start_time__gte=start_of_day,
        start_time__lte=end_of_day,
    ).exclude(student__isnull = True)

    for appointment in tutor_appointments:
        tutor = appointment.tutor
        student_email = appointment.student.user.email
        subject = 'Tutor Appointment Cancellation'
        message = f"Dear {appointment.student.user.first_name}, your tutoring session with {tutor.user.first_name + ' ' + tutor.user.last_name} on {appointment.start_time} was cancelled." #replace with website host
        send_mail(subject, message, 'trentondb0303@gmail.com', [student_email])

    tutor_appointments.delete()
    return redirect('Admin:admin_view_tutor_shifts', tutor_id=tutor.user_id)

