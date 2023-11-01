from django.shortcuts import render
from Apps.TutorApp.models import Tutor, Major
from django.db.models import Q

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