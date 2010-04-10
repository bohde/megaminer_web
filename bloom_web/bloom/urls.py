from django.conf.urls.defaults import *
from views import index
from models import GamePlayerInfo, GameLog
from django.contrib import admin
import tagging


urlpatterns = patterns('',
    url(r'^$', index),
)                       

tagging.register(GamePlayerInfo)
admin.site.register(GamePlayerInfo)
admin.site.register(GameLog)
