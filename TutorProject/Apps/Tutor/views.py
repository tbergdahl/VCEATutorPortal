from django.shortcuts import render, get_object_or_404, redirect
from Apps.TutorApp.models import *
from django.core.mail import send_mail
from django.core.signing import TimestampSigner, BadSignature
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.utils.timezone import make_aware
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
    student_email = appointment.student.user.email
    subject = 'Tutor Appointment Cancellation'
    message = f"Dear {appointment.student.user.first_name}, your tutoring session with {tutor.user.first_name + ' ' + tutor.user.last_name} on {appointment.start_time} was cancelled." #replace with website host
    send_mail(subject, message, 'trentondb0303@gmail.com', [student_email])
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
    message = f"Dear {appointment.student.user.first_name}, please rate your recent tutoring session with {appointment.tutor.user.first_name}. We appreciate your feedback and are always looking to improve your experience. Use the following link: http://127.0.0.1:8000/rate/{signed_token}" #replace with website host
    send_mail(subject, message, 'trentondb0303@gmail.com', [student_email])


    slot = TimeSlot.objects.filter(start_time=appointment.start_time)
    slot.frequency += 1
    slot.save()


    #student stats updating
    student = appointment.student
    student.times_visited += 1
    student.save()

    current_time = datetime.now()

    #update class stats
    tutored_class = appointment.tutored_class
    current_time_aware = make_aware(current_time)
    time_difference = current_time_aware - appointment.start_time
    hours_difference = time_difference.total_seconds() / 3600
    tutored_class.hours_tutored += hours_difference
    tutored_class.save()

    #update tutor stats
    tutor = appointment.tutor
    tutor.hours_tutored += hours_difference
    tutor.save()
    
    
    appointment.delete()
    return redirect('Tutor:view_appointments', tutor.user_id)

@login_required
def view_feedback(request, tutor_id):
    tutor = get_object_or_404(Tutor, user_id=tutor_id)
    return render(request, 'tutor_feedback.html', {'tutor': tutor})