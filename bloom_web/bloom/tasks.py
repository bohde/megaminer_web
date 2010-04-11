"""File for bloom tasks"""

from celery.decorators import task
from celery.task import PeriodicTask
from celery.registry import tasks
from datetime import timedelta

from django.conf import settings
from models import GamePlayerInfo, GameLog

import glob
import contextlib
import string
import os

in_dir = getattr(settings, "BLOOM_IN_PATH", "/tmp/bloom/in")
out_dir = getattr(settings, "BLOOM_OUT_PATH", "/tmp/bloom/out")

class BloomProcessFiles(PeriodicTask):
    run_every = timedelta(seconds=10)

    def run(self, **kwargs):
        logger = self.get_logger(**kwargs)
        for directory in [in_dir, out_dir]:
            if not(os.access(directory, os.F_OK)):
                logger.info("Creating directory %s" % directory)
                try:
                   os.makedirs(directory)
                except:
                   logger.error("Failed at creating directory %s" % directory)
        logger.debug("Processing Directory!")
        for tag_file in glob.iglob('%s/*.tags' % in_dir):
            logger.debug("Looking at file %s" % tag_file)
            game_file = os.path.join(in_dir,string.replace(tag_file, '.tags', '.gamelog'))
            tag_file = os.path.join(in_dir, tag_file)
            process_individual_file.delay(tag_file, game_file, logger)
                   
@task
def process_individual_file(tag_file, game_file, logger):
    gl = GameLog.create_new(game_file, tag_file)
    if gl:
        logger.debug("Game %u created." % gl.number)
    else:
        logger.debug("Game not created.")
    try:
        os.remove(tag_file)
        os.remove(game_file)
    except:
        pass
    return bool(gl)


tasks.register(BloomProcessFiles)
