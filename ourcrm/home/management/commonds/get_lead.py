from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'My custom command to be scheduled'

    def handle(self, *args, **options):
        # Add your task logic here
        self.stdout.write(self.style.SUCCESS('Task executed successfully after 1 minute'))
