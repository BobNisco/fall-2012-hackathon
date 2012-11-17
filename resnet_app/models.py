from django.db import models

# Create your models here.
class Users(models.Model):
	first_name = models.CharField(max_length=100, db_index=True, null=False)
	last_name = models.CharField(max_length=100, db_index=True, null=False)
	grad_year = models.IntegerField()
	employee = models.BooleanField()
	email = models.EmailField()
	phone = models.CharField(max_length=20, null=False)

class Devices(models.Model):
	owner = models.ForeignKey('Users', db_index=True)
	type = models.CharField(max_length=20)
	password = models.CharField(max_length=100)
	username = models.CharField(max_length=100)
	serial = models.CharField(max_length=100)

class Reports(models.Model):
	owner = models.ForeignKey('Users', db_index=True)
	problem = models.CharField(max_length=100)
	description = models.TextField()
	progress = models.CharField(max_length=15)
	completed = models.BooleanField()

class Report_Tech(models.Model):
	report = models.ForeignKey('Reports', db_index=True)
	tech = models.ForeignKey('Users', db_index=True)

class Statuses(models.Model):
	tech = models.ForeignKey('Users', db_index=True)
	message = models.TextField()

class Notifications(models.Model):
	tech = models.ForeignKey('Users', db_index=True)
	type = models.CharField(max_length=20)
	notes = models.TextField()