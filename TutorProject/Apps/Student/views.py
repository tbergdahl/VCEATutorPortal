from django.shortcuts import render
from Apps.TutorApp.models import Tutor, Major
from django.db.models import Q
from .forms import TutorRatingForm, SessionForm
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone


def student_view(request):
    # Get all majors for the filter dropdown
    majors = Major.objects.all()

    # Get query parameters for major and search
    major_name = request.GET.get('major')
    search_query = request.GET.get('search')

    # Start with all tutors
    tutors = Tutor.objects.all()

    # Filter by major if major name is selected
    # Note: This assumes your Major model has a 'name' field that stores the name of the major
    if major_name:
        tutors = tutors.filter(major__name=major_name)  # Filter by the name field of the Major model

    # Search by tutor's name or other fields if search query is provided
    if search_query:
        tutors = tutors.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query)
        )

    context = {
        'tutors': tutors,
        'majors': majors,
        # No need to convert to int, since we are now using the major name
        'selected_major': major_name,
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


# Inside your views.py


def schedule_session(request, tutor_id):
    tutor = get_object_or_404(Tutor, id=tutor_id)
    if request.method == 'POST':
        form = SessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.student = request.user  # assuming the user is a student
            session.tutor = tutor
            session.save()
            return redirect('Student:sessions')  # Redirect to a page where the student can see their sessions
    else:
        # Prepopulate with the current date and time slots
        form = SessionForm(initial={'date': timezone.now().date()})
    return render(request, 'studentSchedule.html', {'form': form, 'tutor': tutor})
