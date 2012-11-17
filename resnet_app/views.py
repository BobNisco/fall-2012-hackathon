# Create your views here.
from models import Device, Report, Report_Tech, Status, Notification
from django.contrib import auth
from django.conf import settings
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404

def index(request):
		return render_to_response('index.html', {'active':'index'})

def login_view(request):
	username = request.POST.get('username', '')
	password = request.POST.get('password', '')
	user = auth.authenticate(username=username, password=password)
	if user is not None and user.is_active:
		# Correct password, and the user is marked "active"
		auth.login(request, user)
		# Redirect to a success page.
		return render_to_response("/account/loggedin/", context_instance=RequestContext(request))
	else:
		# Show an error page
		return render_to_response("/account/invalid/", context_instance=RequestContext(request))

def logout_view(request):
	auth.logout(request)
	# Redirect to a success page.
	return render_to_response("/account/loggedout/")

@login_required
def profile(request):
	user = request.user
	reports = Report.objects.filter(owner=user)
	latest = []
	for report in reports:
		latest.append(Status.objects.filter(report_id=report).order_by('-createdAt')[0])
	return render_to_response('profile.html', {
		'user' : user,
		'reports' : reports,
		'active':'status',
		'latest':latest
	})

@login_required
def view_report(request, reportID):
	report = get_object_or_404(Report, id=reportID)	
	user = request.user
	latest = Status.objects.filter(report_id=reportID).order_by('-createdAt')[0]
	if report:
		if report.owner.id == user.id:
			return render_to_response('view_report.html', {'user' : user,'report' : report, 'latest' : latest})
	return render_to_response('error.html') 
