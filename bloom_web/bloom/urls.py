from django.conf.urls.defaults import *
from views import index, all_logs, top_n, top_n_csv, versus, tagged, all_tagged
from models import GamePlayerInfo, GameLog
import tagging


urlpatterns = patterns('',
    url(r'^$', index, name="index"),
    url(r'^all$', all_logs),
    url(r'^all/tag/(?P<tag_pk>\d+)$', all_tagged, name="all-tagged"),                       
    url(r'^versus/(?P<their_pk>\d+)$', versus, name="versus"),
    url(r'^tagged/(?P<tag_pk>\d+)$', tagged, name="tagged"),
    url(r'^top$', top_n, {'n':3}, name='top-competitors'),
    url(r'^api/top$', top_n_csv, {'n':3}, name='api-top-competitors'),                    
)                       

tagging.register(GamePlayerInfo)
