from django.core.management.base import BaseCommand, CommandError
from ghu_main.email import EmailAPI

class Command(BaseCommand):
    """This command refers to the API in email.py for sending emails in-app"""
    def __init__(self):
        super(Command, self).__init__()

    def add_arguments(self, parser):
        parser.add_argument('subject', type=str)
        parser.add_argument('body', type=str)
        parser.add_argument('recipients', type=str)

    def handle(self, *args, **options):
        EmailAPI.send_email(options['subject'], options['body'], options['recipients'].split(','))
