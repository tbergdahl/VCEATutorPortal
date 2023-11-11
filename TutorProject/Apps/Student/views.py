from django.shortcuts import render
from Apps.TutorApp.models import Tutor, Major, CustomUser
from django.db.models import Q
from .forms import TutorRatingForm
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from Apps.TutorApp.models import TutoringSession

def student_view(request):
    # Get all majors for the filter dropdown
    majors = Major.objects.all()

    # Get query parameters for major and search
    major_id = request.GET.get('major')
    search_query = request.GET.get('search')

    # Start with all tutors
    tutors = Tutor.objects.all()

    # Filter by major if major is selected
    if major_id:
        tutors = tutors.filter(major_id=major_id)

    # Search by tutor's name or other fields if search query is provided
    if search_query:
        tutors = tutors.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query)
        )

    context = {
        'tutors': tutors,
        'majors': majors,
        'selected_major': int(major_id) if major_id else None,
        'search_query': search_query,
    }
    return render(request, 'studentPage.html', context)


def rate_tutor(request, tutor_id):
    tutor = get_object_or_404(Tutor, id=tutor_id)
    if request.method == 'POST':
        form = TutorRatingForm(request.POST, instance=tutor)  # Pass the tutor instance to the form
        if form.is_valid():
            form.save()
            return redirect('Student:student_view')  # Redirect to a success page or the tutor list
    else:
        form = TutorRatingForm(instance=tutor)  # Initialize the form with the tutor instance
    return render(request, 'rateTutor.html', {'form': form, 'tutor': tutor})


def student_view_tutors(request, tutor_id):
    tutor = get_object_or_404(Tutor, id=tutor_id)
    available_appointments = TutoringSession.objects.filter(tutor=tutor, student = None)
    return render(request, 'tutor_available_appointments.html', {'tutor': tutor, 'available_appointments': available_appointments})

def book_appointment(request, session_id):
    session = get_object_or_404(TutoringSession, id=session_id)
    
    if request.user.is_authenticated:
        student_instance = CustomUser.objects.get(pk=request.user.pk).student
        session.student = student_instance
        session.save()
        return redirect('Student:student_view_tutors', tutor_id=session.tutor.id)
    else:
        return redirect('TutorApp:home')

def student_view_appointments(request, student_id):
    student = CustomUser.objects.get(pk=request.user.pk).student
    appointments = TutoringSession.objects.filter(student=student)
    return render(request, 'student_appointments.html', {'appointments': appointments, 'student': student})


