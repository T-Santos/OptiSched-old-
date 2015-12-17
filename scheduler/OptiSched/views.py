from django.http import HttpResponse, HttpResponseRedirect

from django.core.urlresolvers import reverse

from django.template import RequestContext, loader

from django.shortcuts import render_to_response, get_object_or_404, render

from .models import Date,Shift,Person

from .forms import DateForm

import operator
import collections
from datetime import date, timedelta

import pdb

import MakeObject
import ScheduleDateTimeUtilities

'''
def index(request):
	return HttpResponse("Hello, world. You're at the OptiSched index.")
'''
def index(request):

	if(request.GET.get('mybtn')):
   		 MakeObject.make_object( int(request.GET.get('mytextbox')) )
	return render_to_response('OptiSched/index.html')

def create_schedule(request):
	# if this is a POST request we need to process the form data
	if request.method == 'POST':
        	# create a form instance and populate it with data from the request:
        	form = DateForm(request.POST)
        	# check whether it's valid:
        	if form.is_valid():
        		# process the data in form.cleaned_data as required
			new_date = form.cleaned_data['day']
			if(Date.objects.filter(date=new_date)):
				form = DateForm()
				return render(request, 'OptiSched/CreateSchedule.html', {'form': form,
											 'error_msg': "Schedule already exists for this date",
											})
            		# redirect to a new URL:
			else:
				# Create a new schedule with the new_date
				MakeObject.make_schedule( new_date )
            			return HttpResponseRedirect(reverse('OptiSched:day',args=[new_date]))
		# not necessary, form takes care of this		
		else:
			return render(request, 'OptiSched/CreateSchedule.html', {'form': form,
										 'error_msg': "Need a date.",
										})

    	# if a GET (or any other method) we'll create a blank form
    	else:
        	form = DateForm()
		return render(request, 'OptiSched/CreateSchedule.html', {'form': form})

	

def button(request):

	if(request.method == "POST"):
		
        	# Always return an HttpResponseRedirect after successfully dealing
        	# with POST data. This prevents data from being posted twice if a
        	# user hits the Back button.
   		MakeObject.make_object()
        	return HttpResponseRedirect(reverse('OptiSched:employees'))
	else:
		return render(request,'OptiSched/button.html')

def week(request, date):
	
	employee_list = []
    	shifts_per_date = Shift.objects.filter(shift_date=date)
	shifts_per_date = sorted(shifts_per_date, key=operator.attrgetter('employee.last_name'))

	for shift in shifts_per_date:
		employee_list.append(shift.employee)

	employee_list = list(set(employee_list))

    	template = loader.get_template('OptiSched/ViewWeek.html')
    	context = RequestContext(request, {
   				           'employee_list': employee_list,
					   'shifts_per_date': shifts_per_date,
    					   })
  	return HttpResponse(template.render(context))

def employees(request):

	employee_list = Person.objects.all()
	
	template = loader.get_template('OptiSched/EmployeeList.html')
	context = RequestContext(request,{
					  'employee_list': employee_list,
					 })
	return HttpResponse(template.render(context))

def day(request, date):
	work_day = Date.objects.get(date=date)
    	shifts_per_date = Shift.objects.filter(shift_date=date)
	shifts_per_date = sorted(shifts_per_date, key=operator.attrgetter('start_time'))
    	template = loader.get_template('OptiSched/ViewDay.html')
    	context = RequestContext(request, {
					   'work_day': work_day,
					   'work_day_display': work_day.date_display,
   				           'shifts_per_date': shifts_per_date,
					   'hours_in_day': list(range(0,24)),
    					   })
  	return HttpResponse(template.render(context))

def day_person(request, date, Person_id):
    	return HttpResponse("You're looking at the date %s for employee %s." % (date,Person_id))

def employee_week(request, year_num, week_num, employee_id):
	
	week_dates = collections.namedtuple('week_dates', ['start_date','end_date'])

	week_dates = ScheduleDateTimeUtilities.get_dates_from_week(int(year_num),int(week_num))

	temp_shifts_per_week = Shift.objects.filter(shift_date__gte = week_dates[0], shift_date__lte = week_dates[1], employee = employee_id)

	temp_employee = Person.objects.get(pk=employee_id)

	# also defines order of the days of the week
	days_in_week = [0,1,2,3,4,5,6]

	# 0 - 23 = 24
	hours_in_day = range(0,24)

	# for now they are already sorted
	#temp_shifts_per_week = sorted(temp_shifts_per_week,key=operator.attrgetter('shift_date')

	# default in having no shifts
	shifts_per_week = []
	for day in days_in_week:
		shifts_per_week.append("NO_SHIFT")

	# populate where we have shifts
	for day in days_in_week:
		for shift in temp_shifts_per_week:
			if( day == shift.shift_date.date.weekday() ):
				shifts_per_week[day] = shift

	employee_display = temp_employee
	context = RequestContext(request,{'shifts_per_week':shifts_per_week,
					'days_in_week':days_in_week,
					'hours_in_day':hours_in_day,
					'employee_display':employee_display})

	template = loader.get_template('OptiSched/EmployeeWeekView.html')

    	return HttpResponse(template.render(context))
'''
def get_dates_from_week(year,week):

     d = date(year,1,1)
     if(d.weekday()<= 3):
         d = d - timedelta(d.weekday()+1)             
     else:
         d = d + timedelta(7-(d.weekday()+1))
     dlt = timedelta(days = (week-1)*7)
     return d + dlt,  d + dlt + timedelta(days=6)
'''





