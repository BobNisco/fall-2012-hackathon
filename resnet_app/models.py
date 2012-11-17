from django.db import models

# Create your models here.
class Users(models.Model):
	first_name = models.CharField(max_length=100, db_index=True, null=False)
	last_name = models.CharField(max_length=100, db_index=True, null=False)
	grad_year = models.IntegerField()
	employee = models.BooleanField()
	email = models.EmailField()
	phone = models.CharField(max_length=20, null=false)

class Devices(models.Model):
	owner = models.ForeignKey('Users', db_index=true)
	type = models.CharField(max_length=20)
	password = models.CharField(max_length=100)
	username = models.CharField(max_length=100)
	serial = models.CharField(max_length=100)

class Reports(models.Models):
	owner = models.ForeignKey('Users', db_index=true)
	problem = models.CharField(max_length=100)
	description = models.TextField()
	progress = models.CharField(max_length=15)
	completed = models.BooleanField()

class Report_Tech(models.Models):
	report = models.ForeignKey('Reports', db_index=true)
	tech = models.ForeignKey('Users', db_index=true)

class Status(models.Models):
	tech = models.ForeignKey('Users', db_index=true)
	message = models.TextField()

class Notification(models.Models):
	tech = models.ForeignKey('Users', db_index=true)
	type = models.CharField(max_length=20)
	notes = models.TextField()