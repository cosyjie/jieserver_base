import os
from django.core.management import utils
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    def handle(self, *args, **options):
        # 生成新的SECRET_KEY
        new_secret_key = utils.get_random_secret_key()
        key_file_path = os.path.join(settings.APP_FILES,  'conf',  'secretkey.py')

        with open(key_file_path, 'w', encoding='utf-8') as f:
            f.write(f"SECRET_KEY = 'django-insecure-{new_secret_key}'")

        self.stdout.write(
            self.style.SUCCESS('Successfully generated SECRET_KEY ! ')
        )