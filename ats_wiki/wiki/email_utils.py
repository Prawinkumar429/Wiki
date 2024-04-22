from django.core.mail import send_mail
from .models import CustomEmail

def send_custom_email(email_instance):
    recipients = email_instance.recipients.all().values_list('email', flat=True)
    sender_email = email_instance.sender.email
    send_mail(
        email_instance.subject,
        email_instance.body,
        sender_email,
        recipients,
        fail_silently=False,
    )