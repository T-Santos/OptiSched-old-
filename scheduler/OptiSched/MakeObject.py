from datetime import date, datetime, time, timedelta

from OptiSched.models import Person, Date, Shift

import copy
import pdb

def make_object():

	a_person = Person(first_name="James",last_name="Santos")
	a_person.save()

def make_schedule(new_date):

	# create work day and populate fields
	a_work_day = Date(date=new_date)
	current_end_time = a_work_day.day_start_time
	#a_work_day.day_start_time = 

	# shift manage
	all_shifts = []
	active_shifts = []

	# time manage
	work_day_hours = a_work_day.total_hours()
	current_hour =  0
	max_work_hours = 8

	# employee manage
	min_working = 2
	max_working = 6
	more_employees = True

	qs_people = Person.objects.all()
	available_to_work = []

	for person in qs_people:
		available_to_work.append(person.id)	

	# get initial list of employees to work
	while ( len(active_shifts) < min_working):
		if ( len(available_to_work) == 0 ):
			break
		else:
			# get new worker
			a_worker = GetNewEmployee(available_to_work)

			# remove from available to work
			available_to_work.remove(a_worker)
				
			# create new shift for worker and add in fields
			a_shift = Shift(shift_date = a_work_day, employee = GetPersonFromId(a_worker,qs_people))
			a_shift.start_time = current_end_time
			a_shift.end_time = current_end_time
			all_shifts.append(a_shift)
			active_shifts.append(a_shift)		
	
	# go through each hour in the day
	# filling in shifts
	while ( current_hour < (work_day_hours+1) ):

		# remove any shifts that are done
		temp_active_shifts = []
		for active_shift in active_shifts:
			if ( active_shift.hours() == max_work_hours ):
				"do nothing"
			else:
				temp_active_shifts.append(active_shift)

		# update active shifts list
		active_shifts[:] = []
		active_shifts = temp_active_shifts[:]
		temp_active_shifts[:] = []	

		# get employees to work
		while ( len(active_shifts) < min_working):

			if ( len(available_to_work) == 0 ):
				break
			else:
				# get new worker
				a_worker = GetNewEmployee(available_to_work)

				# remove from available to work
				available_to_work.remove(a_worker)
				
				# create new shift for worker and add in fields
				a_shift = Shift(shift_date = a_work_day, employee = GetPersonFromId(a_worker,qs_people))
				a_shift.start_time = current_end_time
				a_shift.end_time = current_end_time
				all_shifts.append(a_shift)
				active_shifts.append(a_shift)
		
		# get and format new end time
		# going to want to pay attention when going into the next day here
		# maybe need to end shift ad midnight and make a new work day?
		current_hour += 1
		temp_datetime = datetime.combine(date.today(), current_end_time) + timedelta(hours=1)
		current_end_time = temp_datetime.time()		
		
		# update active shifts
		for active_shift in active_shifts:
			active_shift.end_time = current_end_time	
					
	# loop through shifts and export
	for shift in all_shifts:
		shift.save()		
	# export work day
	a_work_day.save()
	

def GetPersonFromId(identifier,queryset):
	for person in queryset:
		if (person.id == identifier):
			ret_person = person
			break
	return ret_person

def GetNewEmployee(available_workers):
	# need to make random
	return available_workers[0]

