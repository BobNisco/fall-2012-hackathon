from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Device(models.Model):
	owner = models.ForeignKey(User, db_index=True)
	type = models.CharField(max_length=20, db_index=True)
	password = models.CharField(max_length=100)
	username = models.CharField(max_length=100)
	serial = models.CharField(max_length=100)

class Report(models.Model):
	owner = models.ForeignKey(User, db_index=True)
	device = models.ForeignKey('Device', db_index=True)
	problem = models.CharField(max_length=100)
	description = models.TextField()
	completed = models.BooleanField()
	createdAt = models.DateTimeField(auto_now=True)
	updatedAt = models.DateTimeField(auto_now=True)

class Report_Tech(models.Model):
	report = models.ForeignKey('Report', db_index=True)
	tech = models.ForeignKey(User, db_index=True)

class Status(models.Model):
	tech = models.ForeignKey(User, db_index=True)
	report_id = models.ForeignKey('Report', db_index=True)
	message = models.TextField()
	createdAt = models.DateTimeField(auto_now=True)

class Notification(models.Model):
	tech = models.ForeignKey(User, db_index=True)
	report_id = models.ForeignKey('Report', db_index=True)
	type = models.CharField(max_length=20)
	notes = models.TextField()
	createdAt = models.DateTimeField(auto_now=True)