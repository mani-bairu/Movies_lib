
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from Movies_Apis import tasks
from Movies_Apis.tasks import update_movie_rating

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Movies_lib.settings')

app = Celery('Movies_lib')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

# Schedule the task
app.conf.beat_schedule = {
    'update-movie-rating': {
        'task': 'Movies_Apis.tasks.update_movie_rating',
        'schedule': 300,  # Run every 5 minutes (300 seconds)
    },
}











# to run celery worker
# celery -A your_project worker -l info

#to run celery beat
# celery -A your_project beat -l info

#to run redis server
#redis-server
#redis-cli ping

