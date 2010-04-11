# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from models import GameLog, UserStat
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from tagging.models import Tag
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

@login_required
def versus(request, their_pk):
    them = get_object_or_404(User, pk=their_pk)
    logs = GameLog.ours_with_data(request.user, them)
    return render_to_response('bloom/list.html', {'logs':logs},
                              context_instance=RequestContext(request))  

@login_required    
def tagged(request, tag_pk):
    tag = Tag.objects.get(pk=tag_pk)
    logs = GameLog.mine_with_tag(request.user, tag)
    return render_to_response('bloom/list.html', {'logs':logs},
                              context_instance=RequestContext(request))  

@permission_required('bloom.view_all')
def all_tagged(request, tag_pk):
    tag = Tag.objects.get(pk=tag_pk)
    logs = GameLog.all_with_tag(tag)
    return render_to_response('bloom/list_all.html', {'logs':logs},
                              context_instance=RequestContext(request))  

@permission_required('bloom.view_all')
def stats(request):
    stats = UserStat.objects.all()
    return render_to_response('bloom/stats.html', {'stats':stats},
                              context_instance=RequestContext(request))  

