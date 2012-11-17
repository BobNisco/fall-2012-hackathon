# Create your views here.
from models import Users, Devices, Reports, Report_Tech, Statuses, Notifications

from django.conf import settings
from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404

def index(request):
        return render_to_response('index.html')