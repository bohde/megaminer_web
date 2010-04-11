# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from models import GameLog
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.http import HttpResponse
import csv

@login_required
def index(request):
    logs = GameLog.my_objects(request.user)
    return render_to_response('bloom/list.html', {'logs':logs},
                              context_instance=RequestContext(request))  

@permission_required('bloom.view_all')
def all_logs(request):
    logs = GameLog.objects_with_tags()
    return render_to_response('bloom/list_all.html', {'logs':logs},
                              context_instance=RequestContext(request))  

def top_n(request, n):
    users = User.objects.select_related().order_by('-stats__wins')[:n]
    return render_to_response('bloom/users.html', {'users':users},
                              context_instance=RequestContext(request))  
def top_n_csv(request, n):
    users = User.objects.select_related().order_by('-stats__wins')[:n]
    response = HttpResponse(mimetype='text/csv')
    writer = csv.writer(response)
    writer.writerow([u.username for u in users])
    return response
