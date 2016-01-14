from django import forms

import datetime

class LogInForm(forms.Form):
	
	username = forms.EmailField()
	password = forms.CharField()
#	password = forms.CharField(widget=forms.PasswordInput())
#	class Meta:
#		model = User

class DateForm(forms.Form):
	# get the latest date in the database and increase it by 1 otherwise use today's date
	day = forms.DateField(initial = datetime.date.today)


