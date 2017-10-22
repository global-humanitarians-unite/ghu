import sys
from django.core.management.base import BaseCommand, CommandError
from ghu_global.models import User

class Command(BaseCommand):
    help = "Creates a superuser with a password provided on stdin if it " \
           "does not already exist. Intended for use by ansible scripts, " \
           "not humans. If you're a human, use createsuperuser instead."

    def add_arguments(self, parser):
        parser.add_argument('--user', '-u', default='admin',
                            help='username of admin to create. (default: admin)')

    def handle(self, *args, **options):
        user = options['user']

        # XXX Race condition if the user is created between our check and our
        #     creation
        if User.objects.filter(username=user).exists():
            self.stdout.write("User `{}' already exists, nothing to do"
                              .format(user))
        else:
            password = ''.join(sys.stdin).strip()
            User.objects.create_superuser(user, '', password)
            self.stdout.write("User `{}' created".format(user))
