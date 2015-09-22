from django import forms

import datetime

class DateForm(forms.Form):
	# get the latest date in the database and increase it by 1 otherwise use today's date
	day = forms.DateField(initial = datetime.date.today)


