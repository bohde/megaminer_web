# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import GameLog


def index(request):
    logs = GameLog.objects.all()
    return render_to_response('bloom/list.html', {'logs':logs},
                              context_instance=RequestContext(request))  
