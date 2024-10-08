from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecopiboe.settings')

app = Celery('ecopiboe')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

from celery.schedules import crontab

app.conf.beat_schedule = {
    'cleanup-every-hour': {
        'task': 'gmolver.tasks.cleanup_old_files',
        'schedule': crontab(minute=0, hour='*/1'),
    },
}
