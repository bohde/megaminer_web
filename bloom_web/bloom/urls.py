from django.conf.urls.defaults import *
from views import index
from models import GamePlayerInfo, GameLog
import tagging


urlpatterns = patterns('',
    url(r'^$', index),
)                       

tagging.register(GamePlayerInfo)
