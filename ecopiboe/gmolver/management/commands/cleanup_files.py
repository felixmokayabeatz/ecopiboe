import os
from datetime import datetime, timedelta
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Delete files from uploads folder older than one hour'

    def handle(self, *args, **kwargs):
        upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
        now = datetime.now()

        for filename in os.listdir(upload_dir):
            file_path = os.path.join(upload_dir, filename)
            if os.path.isfile(file_path):
                file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                if now - file_mod_time > timedelta(hours=2):
                    os.remove(file_path)
                    self.stdout.write(self.style.SUCCESS(f'Deleted {file_path}'))
