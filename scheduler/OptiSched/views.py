from django.core.exceptions import ObjectDoesNotExist

from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.decorators import login_required

from django.core.urlresolvers import reverse

from django.template import RequestContext, loader

from django.shortcuts import render_to_response, get_object_or_404, render, redirect

from .models import Date,EmployeeTypeShiftError,Shift,Person

from .forms import NavDateForm,CreateDateForm,CreateDateSpanForm

import operator
import collections
from datetime import datetime,date, timedelta
import datetime as dt

# turning date from external to internal
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format

import pdb

#import MakeObject
import Workday
import ScheduleDateTimeUtilities
import ViewHelperFunctions

TIMESLICE = 30

def home(request):
	context = {}
	template = "home.html"
	return render(request,template,context)

def about(request):
	context = {}
	template = "About.html"
	return render(request,template,context)

def contact(request):
	context = {}
	template = "Contact.html"
	return render(request,template,context)

@login_required
def dashboard(request):
	# TODO: Maybe pass if the user is an employee or manager to show them a different dash
	#pdb.set_trace()
	from_date = dt.date.today()+ dt.timedelta(days=3)
	recently_created_days = Date.objects.filter(date__lte=from_date).order_by('-date')[:7]
	recently_created_shifts = Shift.objects.filter(shift_date__lte=from_date).order_by('-shift_date')[:5]

	recently_viewed_shifts = Shift.objects.filter(shift_date__lte=from_date).order_by('-shift_date')[:5]
	recently_viewed_employees = Person.objects.all()[:5]

	context = {
				'recently_created_days': recently_created_days,
				'recently_created_shifts': recently_created_shifts,
				'recently_viewed_shifts': recently_viewed_shifts,
				'recently_viewed_employees': recently_viewed_employees,
	}
	template = "Dashboard.html"
	return render(request,template,context)

def create_schedule(request):
	template_stay = 'CreateSchedule.html'
	template_redirect = 'OptiSched:ViewManagerDay'

	# if this is a POST request we need to process the form data
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = CreateDateForm(request.POST)
		context = {'CreateDateForm': form}
		# check whether it's valid:
		if form.is_valid():
			# process the data in form.cleaned_data as required
			new_date = date_external = form.cleaned_data['f_date']
			request.session['DATE_STR'] = new_date.isoformat()
			a_workday = Workday.CreateDay(
											date = new_date,
											timeslice = TIMESLICE
											)
			a_workday.GenerateShifts()
			a_workday.Save()
			return HttpResponseRedirect(reverse(template_redirect))
	else:
		form = CreateDateForm()
		context = {'CreateDateForm': form}
	
	return render(request,template_stay,context)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)+1):
        yield start_date + timedelta(n)

def create_date_span(request):

	template = "CreateDateSpan.html"
	template_redirect = "OptiSched:ViewManagerDay"

	if request.method == 'POST':

		form = CreateDateSpanForm(data = request.POST)

		if form.is_valid():

			from_date = form.cleaned_data.get('f_from_date')
			thru_date = form.cleaned_data.get('f_thru_date')
			#from_date_obj = dt.datetime.strptime(from_date, "%Y-%m-%d").date()
			#thru_date_obj = dt.datetime.strptime(thru_date, "%Y-%m-%d").date()

			start_time = form.cleaned_data.get('f_start_time')
			end_time = form.cleaned_data.get('f_end_time')

			#start_time_obj = dt.datetime.strptime(start_time, "%H:%M:%S").time()
			#end_time_obj = dt.datetime.strptime(end_time, "%H:%M:%S").time()


			all_dates = []

			# create and populate dates
			for single_date in daterange(from_date,thru_date):

				a_workday = Workday.CreateDay(
												date = single_date,
												date_start_time = start_time,
												date_end_time = end_time,
												timeslice = TIMESLICE)
				a_workday.GenerateShifts()

				all_dates.append(a_workday)
			
			# save all dates
			for workday in all_dates:
				workday.Save()

			request.session['DATE_STR'] = from_date.isoformat()
			return HttpResponseRedirect(reverse(template_redirect))
	else:        

		form = CreateDateSpanForm(data = request.GET)

	context = {
				'DateSpanForm': form,
			}
	return render(request,template,context)

@login_required
def ViewManagerDay(request):

	template = 'ViewManagerDay.html'

	if request.method == 'POST':
		"View does not accept POSTs"
	else:

		form = NavDateForm(data = request.GET)

		if request.GET.get('navdate',False):
			date = request.GET['navdate']
		else:
			date = dt.datetime.today().strftime("%Y-%m-%d")			

		if date:
			try:
				work_day = Date.objects.get(date=date)
				shifts_per_date = Shift.objects.filter(shift_date=work_day)
				shifts_per_date = sorted(shifts_per_date, key=operator.attrgetter('start_time'))

				date_error_groups = ViewHelperFunctions.ConvertErrorsToGroups(work_day)
				date_error_groups_compressed = ViewHelperFunctions.CompressErrorGroupsToStrings(work_day.date,date_error_groups,TIMESLICE)
				date_error_strings = ViewHelperFunctions.ConvertCompressedErrorsToStrings(date_error_groups_compressed)
				
				context = {
							'NavDateForm': form,
							'work_day_display': work_day.date_display,
	   						'shifts': shifts_per_date,
			   				'date_errors':date_error_strings,
	   					}
			except ObjectDoesNotExist:
				context = {
						'NavDateForm': form,							
						'Error': "No Schedule For Date",
						}
		else:
			context = {
					'NavDateForm': form,
				}

	return render(request,template,context)

def ViewEmployeeWeek(request,employee_id,date):

	if request.method == 'POST':
	
		navform = NavDateForm(request.POST)

		if navform.is_valid():
        	# process the data in form.cleaned_data as required
			#date_external = navform.cleaned_data['navdate']
			#dateformat = DateFormat(date_external)
			#date = dateformat.format('Y-m-d')

			date = navform.cleaned_data['navdate']
			
			if date:
				return redirect('OptiSched:ViewEmployeeWeek',employee_id,date.isoformat())
	else:
		#pdb.set_trace()
		work_day = Date.objects.get(date=date)
		employee = Person.objects.get(pk=employee_id)
		start_end_week_dates = ScheduleDateTimeUtilities.get_dates_from_week(
																				work_day.date.isocalendar()[0],
																				work_day.date.isocalendar()[1]
																			)
		shifts_in_week = Shift.objects.filter(
												shift_date__gte = start_end_week_dates[0],
												shift_date__lte = start_end_week_dates[1],
												employee = employee
											)
		
		navform = NavDateForm(initial={'navdate': date})

		template = 'OptiSched/ViewEmployeeWeek.html'
		context = {
					'employee': employee,
					'shifts': shifts_in_week,
					'NavDateForm': navform,
					'week_start_date':start_end_week_dates[0],
					'week_end_date':start_end_week_dates[1],
				}
		return render(request,template,context)





