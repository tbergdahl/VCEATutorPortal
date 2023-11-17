from django.shortcuts import render, get_object_or_404, redirect
from Apps.TutorApp.models import *
from django.core.mail import send_mail
from django.core.signing import TimestampSigner, BadSignature
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

# Create your views here.
@login_required
def tutor_view(request):
    if not request.user.is_tutor:
        return HttpResponseForbidden("You do not have permission to view this page.")
    return render(request, 'tutorPage.html')

@login_required
def view_appointments(request, tutor_id):
    tutor = get_object_or_404(Tutor, user_id=tutor_id)
    appointments = TutoringSession.objects.filter(tutor=tutor)
    return render(request, 'tutor_appointments.html', {'tutor': tutor, 'appointments':appointments})
@login_required
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(TutoringSession, id=appointment_id)
    tutor = appointment.tutor
    appointment.student = None
    appointment.save()
    return redirect('Tutor:view_appointments', tutor.user_id)
@login_required
def appointment_completed(request, appointment_id):
    appointment = get_object_or_404(TutoringSession, id=appointment_id)

    signer = TimestampSigner()
    tutor_id = appointment.tutor.user_id
    signed_token = signer.sign(f"rate_tutor_{tutor_id}")

    student_email = appointment.student.user.email
    subject = 'Tutoring Session Feedback'
    message = f"Dear {appointment.student.user.first_name}, please rate your recent tutoring session with {appointment.tutor.user.first_name}. We appreaciate your feedback and are always looking to improve your experience. Use the following link: http://127.0.0.1:8000/rate/{signed_token}" #replace with website host
    send_mail(subject, message, 'trentondb0303@gmail.com', [student_email])

    tutor = appointment.tutor
    tutor.minutes_tutored += 20
    tutor.save()
    appointment.delete()
    return redirect('Tutor:view_appointments', tutor.user_id)
@login_required
def view_feedback(request, tutor_id):
    tutor = get_object_or_404(Tutor, user_id=tutor_id)
    return render(request, 'tutor_feedback.html', {'tutor': tutor})