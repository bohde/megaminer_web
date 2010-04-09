"""File for bloom tasks"""

from celery.decorators import task
from celery.task import PeriodicTask
from celery.registry import tasks
from datetime import timedelta

class BloomProcessFiles(PeriodicTask):
    run_every = timedelta(seconds=30)

    def run(self, **kwargs):
        logger = self.get_logger(**kwargs)
        logger.info("Running periodic task!")
                        
tasks.register(BloomProcessFiles)
