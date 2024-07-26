from celery import shared_task
import os
from datetime import datetime, timedelta
from django.conf import settings

@shared_task
def cleanup_old_files():
    upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
    now = datetime.now()

    for filename in os.listdir(upload_dir):
        file_path = os.path.join(upload_dir, filename)
        if os.path.isfile(file_path):
            file_mod_time = datetime.fromtimestamp(os.path.getmtime(file_path))
            if now - file_mod_time > timedelta(hours=0.2):
                os.remove(file_path)
