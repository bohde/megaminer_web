from django.conf.urls.defaults import *
from views import index, all_logs, top_n, top_n_csv
from models import GamePlayerInfo, GameLog
import tagging


urlpatterns = patterns('',
    url(r'^$', index, name="index"),
    url(r'^all$', all_logs),
    url(r'^top$', top_n, {'n':3}, name='top-competitors'),
    url(r'^api/top$', top_n_csv, {'n':3}, name='api-top-competitors'),                    
)                       

tagging.register(GamePlayerInfo)
