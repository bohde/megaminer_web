from django.conf.urls.defaults import *
from views import index, all_logs, top_n
from models import GamePlayerInfo, GameLog
import tagging


urlpatterns = patterns('',
    url(r'^$', index, name="index"),
    url(r'^all$', all_logs),
    url(r'^top$', top_n, {'n':3}, name='top-competitors'),                       
)                       

tagging.register(GamePlayerInfo)
