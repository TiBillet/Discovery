from cryptography.fernet import Fernet
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Salt generation'

    def handle(self, *args, **options):
        self.stdout.write(
            self.style.SUCCESS(
                f"{Fernet.generate_key().decode('utf-8')}"
            ), ending='\n')
