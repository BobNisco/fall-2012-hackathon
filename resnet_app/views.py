# Create your views here.
import datetime
from models import User,Device, Report, Report_Tech, Status, Notification
from django.contrib import auth
from django.conf import settings
from django.utils import simplejson
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404

def index(request):
	user = request.user
	reports = Report.objects.filter(completed=False).order_by('-createdAt')
	reports_length = len(reports)
	now = datetime.datetime.now()
	now_day = now.strftime("%A")
	return render_to_response('index.html', {
		'user' : user,
		'reports' : reports,
		'reports_length' : reports_length,
		'now' : now,
		'now_day' : now_day,
		'active':'index', 
	})

def login_view(request):
	username = request.POST.post('username', '')
	password = request.POST.post('password', '')
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
	return render_to_response("/reports/")

@login_required
def profile(request):
	user = request.user
	reports = Report.objects.filter(owner=user).order_by('-createdAt')
	devices = Device.objects.filter(owner=user)
	statuses = {}
	for report in reports:
		statuses[report.id] = Status.objects.filter(report=report).order_by('-createdAt')
	latest_statuses = {}
	for report in reports:
		if statuses[report.id]:
			latest_statuses[report.id] = statuses[report.id][0]
	return render_to_response('profile.html', {
		'user' : user,
		'reports' : reports,
		'devices' : devices,
		'active' : 'status',
		'statuses' : statuses,
		'latest_statuses' : latest_statuses,
	})

def office_status(request):
	user = request.user
	reports = Report.objects.filter(completed=False).order_by('-createdAt')
	reports_length = len(reports)
	now = datetime.datetime.now()
	now_day = now.strftime("%A")
	is_open = False
	if (now.hour > 10 and now.hour < 19 and now_day != 'Friday') or (now.hour > 10 and now.hour < 17 and now_day == 'Friday'):
		is_open = True
	return render_to_response('office_status.html', {
		'user' : user,
		'reports' : reports,
		'reports_length' : reports_length,
		'now' : now,
		'now_day' : now_day,
		'active':'office',
		'open' : is_open,
	})

@login_required
def view_report(request, reportID):
	report = get_object_or_404(Report, id=reportID)	
	user = request.user
	statuses = Status.objects.filter(report_id=reportID).order_by('-createdAt')
	latest = ''
	if statuses:
		latest = statuses[0]
	if report:
		if report.owner.id == user.id:
			return render_to_response('view_report.html', {
				'user' : user,
				'report' : report,
				'statuses' : statuses,
				'latest' : latest,
				'active' : 'status',
			})
	else:
		return render_to_response('error.html') 

@login_required
def cpanel(request):
	user = request.user
	reports = Report.objects.all()
	open = len(reports.filter(completed = False))
	closed = len(reports.filter(completed = True))
	numReports = len(reports)
	return render_to_response('cpanel/cpanel.html', {
			'numReports' : numReports, 
			'user' : user, 
			'open' : open, 
			'closed' : closed})

@login_required
def cpanel_open(request):
	user = request.user
	device_choices = Device.get_device_choices(Device())
	os_choices = Device.get_os_choices(Device())
	problem_choices = Report.get_problem_choices(Report())
	return render_to_response('cpanel/open.html', {
			'user' : user, 
			'device_choices' : device_choices, 
			'os_choices' : os_choices, 
			'problem_choices' : problem_choices
			}, context_instance=RequestContext(request))

@login_required
def cpanel_submit(request):
	name = request.POST['name']
	phone = request.POST['phone']
	email = request.POST['email']
	type = request.POST['device']
	os = request.POST['os']
	problem = request.POST['problem']
	description = request.POST['description']
	deviceObj = Device()
	report = Report()
	usersWithSameEmail = User.objects.filter(email=email)
	for u in usersWithSameEmail:
		# If user exists, don't create a new one
		if u.email == email:
			deviceObj.owner = u
			deviceObj.device = os
			deviceObj.type = type
			deviceObj.save()
			
			report.owner = u
			report.device = deviceObj
			report.description = description
			report.problem = problem
			report.completed = False
			report.save()
			
			reports = Report.objects.all()
			return render_to_response('test.html', {
				'reports' : reports,
			})
	# Otherwise create a new one
	return render_to_response('test.html', {'email' : email})

def find_device(request):
	if request.is_ajax():
		id = request.POST['id']
		device = Device.objects.get(id=id)
		reports = Report.objects.filter(device=device)
		if device:
			return render_to_response('device_modal.html', {
				'device' : device,
				'reports' : reports,
			})
	else:
		return 'error'
