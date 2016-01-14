from django.core.exceptions import ObjectDoesNotExist

from django import forms
from .models import Date

import datetime as dt
import pdb

class LogInForm(forms.Form):
	
	username = forms.EmailField()
	password = forms.CharField()
	other = forms.CharField()
#	password = forms.CharField(widget=forms.PasswordInput())
#	class Meta:
#		model = User

class CreateDateForm(forms.Form):
	# get the latest date in the database and increase it by 1 otherwise use today's date
	f_createdate = forms.DateField(initial = dt.datetime.today().strftime("%Y-%m-%d"))

class NavDateForm(forms.Form):
	# get the latest date in the database and increase it by 1 otherwise use today's date
		
	try:
    		#Date = Date.objects.get(date=dt.datetime.today().strftime("%Y-%m-%d"))
		#navdate = forms.DateField(initial = Date)
		# Date = most recent in db
		navdate = forms.DateField(initial = dt.datetime.today().strftime("%Y-%m-%d"))
	except ObjectDoesNotExist:
    		navdate = forms.DateField()
		


