from django.core.mail import send_mail
from django.conf import settings

def send_admin_email(complaint):
    """Send email to admin when a new complaint is submitted."""
    subject = f"New Complaint #{complaint.id} - {complaint.name}"
    message = (
        f"A new complaint has been submitted.\n\n"
        f"ID: #{complaint.id}\n"
        f"Name: {complaint.name}\n"
        f"Course: {complaint.course_code}\n"
        f"Office: {complaint.submission_office}\n"
        f"Complaint: {complaint.complaint_text}\n\n"
        f"View: https://kwanyise.pythonanywhere.com/admin/"
    )
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [settings.ADMIN_EMAIL],
        fail_silently=True,
    )

def send_student_email(complaint, snapshot_url):
    """Send email to student when complaint is submitted."""
    if not complaint.email:
        return
    subject = f"Your complaint (#{complaint.id}) has been submitted"
    message = (
        f"Hello {complaint.name},\n\n"
        f"Your complaint ({complaint.course_code}) has been submitted to {complaint.submission_office}.\n"
        f"You can view the proof of submission here:\n{snapshot_url}\n\n"
        f"Thank you for using our service."
    )
    send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [complaint.email],
        fail_silently=True,
    )