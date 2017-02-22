"""Tasks to perform periodic tasks with remotes."""

from django_celery_beat.models import IntervalSchedule, PeriodicTask
from celery import Celery
from celery.utils.log import get_task_logger

import maya


celery_app = Celery()
logger = get_task_logger(__name__)


@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Ensure periodic tasks are present in the DB."""
    logger.info("Configuring periodic tasks.")
    logger.debug('Sender: %s; kwargs: %s', sender, kwargs)

    schedule, created = IntervalSchedule.objects.get_or_create(every=10, period=IntervalSchedule.MINUTES)

    pertask, created = PeriodicTask.objects.get_or_create(interval=schedule, name='Harvest Remotes', task='remotes.tasks.harvest_sources')
    logger.debug("Got periodic task: %s", pertask)

    if created:
        logger.debug('Newly created, set expiry.')
        pertask.expires = maya.now().add(minutes=30).datetime()
        pertask.save()
    else:
        logger.info("Deleting old periodic task and creating a new one.")
        pertask.delete()
        PeriodicTask.objects.create(interval=schedule, name='Harvest Remotes', task='remotes.tasks.harvest_sources', expires=maya.now().add(minutes=30).datetime())


@celery_app.task
def harvest_sources():
    """Get a new batch of data from all sources."""
    from .models import Source
    for source in Source.objects.all():
        logger.info("Harvesting from Source: %s", source)
        harvester = source.harvester()
        for post in harvester.harvest():
            logger.info("Got new Post: %s", post)
            post.save()
