from django.core.mail import send_mail

class EmailAPI(object):
    """docstring for EmailAPI."""
    def __init__(self):
        super(EmailAPI, self).__init__()

    def send_email(subject, message, recipients):
        send_mail(
            subject,
            message,
            'contact@globalhumanitariansunite.org',
            recipients,
            fail_silently=False,
        )
