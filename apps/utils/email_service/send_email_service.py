import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Root.settings')
django.setup()

# Now you can safely use Django settings and features
from django.conf import settings
print(settings.EMAIL_BACKEND)
from django.core.mail import send_mail


def send_gmail_email():
    subject = "Welcome to Our Service"
    message = "Hello, thanks for joining us!"
    recipient_list = ["mwakionyambu57@gmail.com"]

    send_mail(
        subject,
        message,
        from_email=None,  # Uses DEFAULT_FROM_EMAIL in settings.py
        recipient_list=recipient_list,
        fail_silently=False,  # Set to True to avoid raising errors on failure
    )

send_gmail_email()
print('sent!')
