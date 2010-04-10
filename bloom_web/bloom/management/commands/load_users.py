from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = "Import a list of users and passwords into the system."
    args = "users"
    
    def handle(self, *args, **options):
        if not(args):
            raise CommandError("Require a file name for the argument")
        for arg in args:
            try:
                with open(arg) as f:
                    for line in f:
                        user, password = line.split()
                        try:
                            User.objects.get(username=user)
                            print "%s already exists, not adding." % user
                        except User.DoesNotExist:
                            print "Adding new user %s" % user
                            u = User.objects.create_user(user, 'test@example.com', password)
                            u.save()
            except IOError:
                raise CommandError("Couldn't open %s." % arg)
