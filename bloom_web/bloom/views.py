# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import GameLog
from django.contrib.auth.decorators import login_required, permission_required

@login_required
def index(request):
    logs = GameLog.my_objects(request.user)
    return render_to_response('bloom/list.html', {'logs':logs},
                              context_instance=RequestContext(request))  

@permission_required('bloom.view_all')
def all_logs(request):
    logs = GameLog.objects_with_tags()
    return render_to_response('bloom/list.html', {'logs':logs},
                              context_instance=RequestContext(request))  

