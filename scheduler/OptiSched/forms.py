from django.core.exceptions import ObjectDoesNotExist

from django.conf import settings
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

class NavDateForm(forms.Form):
	# get the latest date in the database and increase it by 1 otherwise use today's date
		
	try:
    		#Date = Date.objects.get(date=dt.datetime.today().strftime("%Y-%m-%d"))
		#navdate = forms.DateField(initial = Date)
		# Date = most recent in db
		navdate = forms.DateField(initial = dt.datetime.today().strftime("%Y-%m-%d"))
	except ObjectDoesNotExist:
    		navdate = forms.DateField()

class CreateDateForm(forms.Form):
	# get the latest date in the database and increase it by 1 otherwise use today's date
	f_date = forms.DateField(initial = dt.datetime.today().strftime("%Y-%m-%d"))

	f_start_time = forms.TimeField(input_formats=settings.TIME_INPUT_FORMATS)
	f_end_time = forms.TimeField(input_formats=settings.TIME_INPUT_FORMATS)

	def clean(self):
		cleaned_data = super(CreateDateForm,self).clean()

		start_time = cleaned_data.get('f_start_time',False)
		end_time = cleaned_data.get('f_end_time',False)

		if not start_time:
			msg = "Start Time is required"
			raise forms.ValidationError(msg)
		elif not end_time:
			msg = "End Time is required"
			raise forms.ValidationError(msg)
		elif not start_time < end_time:
			msg = "End Time must fall affter Start Time"
			raise forms.ValidationError(msg)

class CreateDateSpanForm(forms.Form):

	f_from_date = forms.DateField()
	f_thru_date = forms.DateField()

	f_start_time = forms.TimeField(input_formats=settings.TIME_INPUT_FORMATS)
	f_end_time = forms.TimeField(input_formats=settings.TIME_INPUT_FORMATS)

	def clean(self):
		cleaned_data = super(CreateDateSpanForm,self).clean()

		from_date = cleaned_data.get('f_from_date')
		thru_date = cleaned_data.get('f_thru_date')

		start_time = cleaned_data.get('f_start_time')
		end_time = cleaned_data.get('f_end_time')

		if not from_date:
			msg = "From Date is required"
			self.add_error('f_from_date',msg)
		
		if not thru_date:
			msg = "Thru Date is required"
			self.add_error('f_thru_date',msg)

		if not from_date <= thru_date:
			msg = "From Date must fall before Thru Date"
			raise forms.ValidationError(msg)

		if not start_time < end_time:
			msg = "End Time must fall affter Start Time"
			raise forms.ValidationError(msg)