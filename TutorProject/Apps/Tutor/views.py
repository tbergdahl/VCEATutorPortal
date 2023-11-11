from django.shortcuts import render, get_object_or_404, redirect
from Apps.TutorApp.models import *

# Create your views here.
def tutor_view(request):
    return render(request, 'tutorPage.html')

def view_appointments(request, tutor_id):
    tutor = get_object_or_404(Tutor, id=tutor_id)
    appointments = TutoringSession.objects.filter(tutor=tutor)
    return render(request, 'tutor_appointments.html', {'tutor': tutor, 'appointments':appointments})

def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(TutoringSession, id=appointment_id)
    tutor = appointment.tutor
    appointment.student = None
    appointment.save()
    return redirect('Tutor:view_appointments', tutor.id)