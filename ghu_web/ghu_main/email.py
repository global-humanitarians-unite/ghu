from django.core.mail import send_mail
from django.conf import settings

class EmailAPI(object):
    """This API provides methods for managing mail through the app"""
    def __init__(self):
        super(EmailAPI, self).__init__()

    def send_email(subject, message, recipients):
        send_mail(
            subject,
            message,
            settings.EMAIL_SOURCE,
            recipients,
            fail_silently=False,
        )
