import os

from django.core.management.base import BaseCommand, CommandError
from cryptography.fernet import Fernet

from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        make_key = Fernet.generate_key()
        key_file_path = os.path.join(settings.APP_FILES,  'conf',  'encryptionkey.py')

        with open(key_file_path, 'w', encoding='utf-8') as f:
            f.write(f"ENCRYPT_KEY = {make_key}")

        self.stdout.write(
            self.style.SUCCESS('Successfully generated encryption key ! ')
        )