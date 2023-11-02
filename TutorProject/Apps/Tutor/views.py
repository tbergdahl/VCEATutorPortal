from django.shortcuts import render

# Create your views here.
def tutor_view(request):
    return render(request, 'tutorPage.html')