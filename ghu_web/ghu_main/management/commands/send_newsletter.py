from django.core.management.base import BaseCommand, CommandError
from ghu_main.email import EmailAPI

class Command(BaseCommand):
    """docstring for Command."""
    def __init__(self):
        super(Command, self).__init__()

    def handle(self, *args, **options):
        EmailAPI.send_email("Weekly Newsletter", "I am the email Body", ["xarlyle0@gmail.com"])
