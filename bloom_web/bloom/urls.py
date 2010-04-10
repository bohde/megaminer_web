from django.conf.urls.defaults import *
from views import index, all_logs
from models import GamePlayerInfo, GameLog
import tagging


urlpatterns = patterns('',
    url(r'^$', index),
    url(r'^all$', all_logs),                       
)                       

tagging.register(GamePlayerInfo)
