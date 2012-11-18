from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Device(models.Model):
	DEVICE_CHOICES = (
		("l", "Laptop"),
		("d", "Desktop"),
		("m", "Mobile"),
	)
	OS_CHOICES = (
		("wx", "Windows XP"),
		("w7", "Windows 7"),
		("w8", "Windows 8"),
		("mc", "Mac OS X"),
		("io", "iOS"),
		("an", "Android"),
		("bb", "BlackBerry"),
		("wp", "Windows Phone"),
		("ot", "Other"),
	)
	owner = models.ForeignKey(User, db_index=True)
	type = models.CharField(max_length=2, choices=DEVICE_CHOICES, db_index=True)
	os = models.CharField(max_length=2, choices=OS_CHOICES, db_index=True)
	username = models.CharField(max_length=100, null=True, blank=True)
	password = models.CharField(max_length=100, null=True, blank=True)
	serial = models.CharField(max_length=100, null=True, blank=True)
	
	def __unicode__(self):
		return '%s\'s %s' %(self.owner.username, self.get_type_display())

class Report(models.Model):
	owner = models.ForeignKey(User, db_index=True)
	device = models.ForeignKey('Device', db_index=True)
	problem = models.CharField(max_length=100)
	description = models.TextField()
	completed = models.BooleanField()
	createdAt = models.DateTimeField(auto_now=True)
	updatedAt = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return '%s\'s %s - %s' %(self.owner.username, self.device.get_type_display(), self.problem)

class Report_Tech(models.Model):
	report = models.ForeignKey('Report', db_index=True)
	tech = models.ForeignKey(User, db_index=True)

class Status(models.Model):
	MESSAGE_CHOICES = (
		("c", "Checked In"),
		("i", "In Progress"),
		("f", "Fixed"),
		("n", "User Notified"),
		("p", "Picked Up")
	)
	tech = models.ForeignKey(User, db_index=True)
	report = models.ForeignKey('Report', db_index=True)
	message = models.CharField(max_length=1, choices=MESSAGE_CHOICES)
	note = models.TextField()
	createdAt = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return '%s\'s %s - %s - %s' %(self.report.owner.username, self.report.device.get_type_display(), self.report.problem, self.get_message_display())	

class Notification(models.Model):
	NOTIFICATION_TYPES = (
		("p", "Phone Call"),
		("s", "SMS"),
		("e", "Email"),
	)
	tech = models.ForeignKey(User, db_index=True)
	report = models.ForeignKey('Report', db_index=True)
	type = models.CharField(max_length=20)
	notes = models.TextField()
	createdAt = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return '%s\'s %s to %s' %(self.tech.username, self.get_type_display(), self.report.owner.username)
