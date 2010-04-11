from django.contrib import admin
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from tagging.models import Tag
from django.core.files import File
from django.core.files.storage import FileSystemStorage
import hashlib
import shutil
import string
import os
import logging
import itertools
logging.basicConfig(level=logging.DEBUG)


in_dir = getattr(settings, "BLOOM_IN_PATH", "/tmp/bloom/in")
out_dir = getattr(settings, "BLOOM_OUT_PATH", "/tmp/bloom/out")
media_path = getattr(settings, "BLOOM_MEDIA_PATH", "/logs/")

fs = FileSystemStorage(location=out_dir, base_url=media_path)

def md5_for_file(file_name, block_size=2**20):
    try:
        with open(file_name) as f:
            md5 = hashlib.md5()
            while True:
                data = f.read(block_size)
                if not data:
                    break
                md5.update(data)
            return md5.hexdigest()
    except IOError:
        return None

def read_tag_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        num, p1_name, p2_name, winner_index = lines[0][0:-1].split(', ')
        num = int(num)
        winner_index = int(winner_index)

        p1_name = string.replace(p1_name, ' ', '')
        p2_name = string.replace(p2_name, ' ', '')

        p1 = GamePlayerInfo.objects.create(player=(User.objects.get(username__iexact=p1_name)),
                                           winner=(winner_index==0))
        Tag.objects.update_tags(p1, lines[1])

        p2 = GamePlayerInfo.objects.create(player=(User.objects.get(username__iexact=p2_name)),
                                           winner=(winner_index==1))
        Tag.objects.update_tags(p2, lines[2])

        return num, p1, p2

class GamePlayerInfo(models.Model):
    player = models.ForeignKey(User)
    winner = models.BooleanField()

    def __unicode__(self):
        return "%s (%u)" % (self.player.username, self.pk)
    
class GameLog(models.Model):
    game_hash = models.CharField(max_length=256)
    file = models.FileField(upload_to=out_dir, storage=fs)
    number = models.IntegerField()
    p1 = models.OneToOneField(GamePlayerInfo, related_name='p1_log_set')
    p2 = models.OneToOneField(GamePlayerInfo, related_name='p2_log_set')

    class Meta:
        ordering = ["-id"]
        
    def __unicode__(self):
        return "%s vs. %s" % (self.p1.player.username, self.p2.player.username)

    @classmethod
    def mine(cls, user):
        try:
            return cls.objects.filter(models.Q(p1__player=user) | models.Q(p2__player=user)).select_related()
        except GameLog.DoesNotExist:
            return None

    @staticmethod
    def my_objects(user):
        objs = GameLog.mine(user)
        def add_tags(qs):
            for q in qs:
                q.tags = set(itertools.chain.from_iterable(p.tags for p in [q.p1, q.p2] if p.player==user))
                yield q
            return
        def add_win_status(qs):
            for q in qs:
                if q.p1.player==user and q.p2.player==user:
                    q.win_status = "tie"
                else:
                    if q.p1.player==user:
                        q.win_status = ["loss", "win"][q.p1.winner]
                    else:
                        q.win_status = ["win", "loss"][q.p1.winner]
                yield q
            return
        return add_win_status(add_tags(objs))

    @staticmethod
    def objects_with_tags():
        objs = GameLog.objects.all()
        def add_tags(qs):
            for q in qs:
                q.tags = set(itertools.chain.from_iterable(p.tags for p in [q.p1, q.p2]))
                yield q
            return
        def winner(qs):
            for q in qs:
                q.win_status = q.p1.player.username if q.p1.winner else q.p2.player.username
                yield q
            return
        return winner(add_tags(objs))
    

    @staticmethod
    def create_new(log_file, tag_file):
        game_hash = md5_for_file(log_file)
        if not(game_hash):
            """The file doesn't exist"""
            return None
        try:
            number, p1, p2 = read_tag_file(tag_file)
        except (IOError, User.DoesNotExist):
            return None

        """Copy the file to the output directory"""
        new_file_location = os.path.join(out_dir, "%s.gamelog"%game_hash)
        shutil.move(log_file, new_file_location)

        gl = GameLog(game_hash=game_hash,
                     number=number,
                     p1=p1,
                     p2=p2)
        gl.file.name = '%s.gamelog'%game_hash
        gl.save()
        return gl

