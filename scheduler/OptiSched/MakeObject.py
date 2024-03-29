#from datetime import date, datetime, time, timedelta

import datetime
import time
import random
import collections

from OptiSched.models import *
import ScheduleDateTimeUtilities

import copy
import pdb
import random

# Error List
make_schedule_errors = {}

# pdb.set_trace()

'''
****************************************************

****************************************************
'''	
def make_object():

	a_person = Person(first_name="James",last_name="Santos")
	a_person.save()

'''
****************************************************

****************************************************
'''	
def make_schedule(new_date):

	# create work day and populate fields
	a_work_day = Date(date = new_date)		# init workday
	current_end_time = a_work_day.day_start_time	# init the current end time

	# shift manage
	all_shifts = []    				# includes all shifts that have started
	active_shifts = []  				# includes the current active shifts

	# time manage
	work_day_hours = a_work_day.total_hours()	# get the total hours in the work day
	current_hour =  0				# to store the current hour that we are working on

	qs_all_employees = Person.objects.all()		# get all the employees

	all_employees = []				# list of all of the employees
	for person in qs_all_employees:
		all_employees.append(person)

	# go through each hour in the day filling in shifts
	while ( current_hour < work_day_hours ):	

		# get employees to work
		while ( MoreShiftsNeeded(a_work_day,
				         current_end_time,
					 active_shifts) ):
		
			# get current active and existing shifts
			temp_unavailable_employees = []
			
			# Get unavailable (already working or already worked) employees
			for existing_shifts in all_shifts:
				temp_unavailable_employees.append(existing_shifts.employee)
			for existing_shifts in active_shifts:
				if existing_shifts.employee not in temp_unavailable_employees:
					temp_unavailable_employees.append(existing_shifts.employee)
		
		
			# get employee types needed
			employee_types_needed_for_shifts = MoreShiftsNeeded(a_work_day,
				         				current_end_time,
					 				active_shifts)
		
			# Get a new needed shift
			new_employee_for_shift = GetNewEmployee(a_work_day,
								current_end_time,
								temp_unavailable_employees,
								employee_types_needed_for_shifts)
		
			if ( not(new_employee_for_shift) ):

				# if there are no new employees for shifts but we needed some log an error
				if (employee_types_needed_for_shifts):
					Log_Schedule_Error("Employee",employee_types_needed_for_shifts)
					error_dt = datetime.datetime.combine(a_work_day.date,current_end_time)
					Log_Schedule_Error("DateTime",str(error_dt) + " Employees Needed")
					Log_Schedule_Error(error_dt,employee_types_needed_for_shifts)
					
				# TODO: Set flag if we cant create a new shift
				break
			else:				
				# create the new shift
				a_shift = Shift(shift_date = a_work_day,
								employee = new_employee_for_shift[0],
								shift_employee_type = new_employee_for_shift[1])
			
				a_shift.start_time = current_end_time
				a_shift.end_time = current_end_time

				# update lists of existing shifts
				all_shifts.append(a_shift)
				active_shifts.append(a_shift)
		
		# increment end time
		current_hour += 1
		temp_datetime = datetime.datetime.combine(datetime.date.today(), current_end_time) + datetime.timedelta(hours=1)
		current_end_time = temp_datetime.time()		
		
		# update active shifts' end time
		for active_shift in active_shifts:
			active_shift.end_time = current_end_time
		
		# remove actively working employees that are no longer needed
		active_shifts = RemoveActiveShifts(active_shifts,a_work_day,current_end_time)
					
	# loop through shifts and export
	for shift in all_shifts:
		shift.save()		
	# export work day
	a_work_day.save()

'''
****************************************************

****************************************************
'''	
def MoreShiftsNeeded(a_work_day,current_end_time,active_shifts):

	# get dict of requirement types keyed by the type of employee (manager, cook, eye dr., etc)
	employee_type_requirements = {}
	employee_type_requirements = GetEmployeeTypeRequirements(a_work_day.date,current_end_time)

	# final list of employee type requirements 	
	employee_type_requirements_needed = []

	# make sure we have at least some type of requirement? 
	# if not are they only a morning, 6-11 everybody go home 5-12 type of business
	# pdb.set_trace()
	if ( not(employee_type_requirements) ):
		# maybe not log error since employees dont start until 8 and the day starts at 0:00
		"Log as an error"
	else:

		if( not(active_shifts) ):
			
			# if there are no active shifts, we need to fill all spots defined by the requirements
			# [0] is the most relevant time since we append them [most,relevant,to,least,relevant]
			for temp_employee_type, temp_employee_requirement_list in employee_type_requirements.items():
				employee_type_requirements_needed.append(temp_employee_requirement_list[0])
		else:
			# get the counts for all the active working employee types
			active_type_counts = {}
			for active_shift in active_shifts:
				active_type_counts[active_shift.shift_employee_type.et_type] = active_type_counts.get(active_shift.shift_employee_type.et_type,0) + 1

			# for all the requirements, if they aren't filled make sure we return that we need them
			for temp_employee_type, temp_employee_requirement_list in employee_type_requirements.items():

				if( active_type_counts.get(temp_employee_type,0) < temp_employee_requirement_list[0].etr_employee_type_count ):
					employee_type_requirements_needed.append(temp_employee_requirement_list[0])
				else:
					"nothing"
	#pdb.set_trace()	
	# return list of employee types or false
	if( employee_type_requirements_needed ):
		return employee_type_requirements_needed
	else:
		return False	

'''
****************************************************

****************************************************
'''	
def GetEmployeeTypeRequirements(date,time):

	# form current datetime 
	now = datetime.datetime.combine(date,time)

	# form beginning of the day
	begin_of_day = datetime.datetime.combine(date,datetime.time(0,0,0))
	
	#-----------------------------
	# get employee requirements
	# we get the request from most recent (across all types) to least recent
	# and then later sort them out by type. For each type [0] will be the most 
	# recent since the most recent gets put in first

	# given the current date and time see if there are any
	# override specific datetime requirements
	emp_req_ovrs = EmployeeRequirementDateTimeOverride.objects.filter(
								erd_datetime__gte = begin_of_day,
								erd_datetime__lte = now
								).order_by(
								'-erd_datetime')

	# if there are no employee requirement overrides, check for requirements for the 
	# given day of the week and time
	if (not emp_req_ovrs):
		emp_reqs = EmployeeRequirementTime.objects.filter(
								day_of_week = date.weekday(),
								ert_start_time__lte = now
								).order_by(
								'-ert_start_time')

	# Make a map/dictionary of employee type reqirements and types needed checking
	'''
	{ Managers , [req 1,req 2] }
	{ Cooks	   , [req 1,req 2] }
	'''
	employee_type_requirements = {}
		
	# Divvy the requirements out by employee type
	if emp_req_ovrs:
		for emp_req_ovr in emp_req_ovrs:
    			if emp_req_ovr.erd_requirement.etr_employee_type.et_type in employee_type_requirements:
        			# append the new number to the existing array at this slot
        			employee_type_requirements[emp_req_ovr.erd_requirement.etr_employee_type.et_type].append(emp_req_ovr.erd_requirement)
    			else:
        			# create a new array in this slot
        			employee_type_requirements[emp_req_ovr.erd_requirement.etr_employee_type.et_type] = [emp_req_ovr.erd_requirement]
	elif emp_reqs:
		for emp_req in emp_reqs:
    			if emp_req.ert_requirement.etr_employee_type.et_type in employee_type_requirements:
        			# append the new number to the existing array at this slot
        			employee_type_requirements[emp_req.ert_requirement.etr_employee_type.et_type].append(emp_req.ert_requirement)
    			else:
        			# create a new array in this slot
        			employee_type_requirements[emp_req.ert_requirement.etr_employee_type.et_type] = [emp_req.ert_requirement]

	return employee_type_requirements

'''
****************************************************

****************************************************
'''	
def GetNewEmployee(cur_date,
                   cur_time,
                   unavailable_workers,
		   emp_types_needed):

	#------
	year_num = cur_date.date.year
	week_num = cur_date.week()
	
	# get all employees
	qs_all_employees = Person.objects.all()
	available_employees = []

	# get all available employees
	for emp in qs_all_employees:
		if not emp in unavailable_workers:
			available_employees.append(emp)

	# get just the employee types needed	
	temp_emp_types_needed = []
	for emp_type_needed in emp_types_needed:
		temp_emp_types_needed.append(emp_type_needed.etr_employee_type)

	
	# ***************************************************************
	# Need to weed out all available employees that are not qualified
	# to work roles for shifts that need to be filled
	# someone who is only a cook cannot fill a manger's shift

	temp_available_employees = []
   	del temp_available_employees[:]
	temp_available_employees = copy.deepcopy(available_employees)

	for available_employee in temp_available_employees:
		
		temp_person_employee_types = []		
		temp_person_employee_types = PersonEmployeeType.objects.filter(pet_employee = available_employee)
		
		temp_employee_types = [] 
		for temp_person_employee_type in temp_person_employee_types:
			temp_employee_types.append(temp_person_employee_type.pet_employee_type)
		
		#-----------------------
		# check if at least one type exists in each list
		temp_et_intersect = []
		temp_et_intersect = list( set.intersection( set(temp_employee_types),set(temp_emp_types_needed) ) )
		
		if not temp_et_intersect:
			available_employees.remove(available_employee)

		#-------------------------
		# check to see if the available employee has already worked enough hours for a full week
		week_dates = collections.namedtuple('week_dates', ['start_date','end_date'])
		week_dates = ScheduleDateTimeUtilities.get_dates_from_week(int(year_num),int(week_num))

		temp_emp_existing_shifts_in_week = Shift.objects.filter(shift_date__gte = week_dates[0],
									shift_date__lte = week_dates[1],
									employee = available_employee.id)
		hours_worked_in_week = 0
		for existing_shift in temp_emp_existing_shifts_in_week:
			hours_worked_in_week += existing_shift.hours()

		# if the employee has worked total hours per week; remove them
		if (hours_worked_in_week >= available_employee.person_max_hours_per_week):
			if ( available_employee in available_employees):
				available_employees.remove(available_employee)
		# if an employee's hours left to work in a week is less than a minimum shift; remove them
		elif (available_employee.person_min_hours_per_shift > (available_employee.person_max_hours_per_week - hours_worked_in_week) ):
			if ( available_employee in available_employees):
				available_employees.remove(available_employee)
		# Remove available employees who are available to work based on hours left in the week
		# but have a restriction coming up in the same day that is sooner than
		# a minimum shift. 
		# For example, the current hour is 10 they can't work at 12 or later and min shift = 4hrs
		elif( HoursUntilCantWork(available_employee,cur_date.date,cur_time) < available_employee.person_min_hours_per_shift ):
			if ( available_employee in available_employees):
				available_employees.remove(available_employee)
		
        # Get all DateTimeRequest
	qs_all_requests = DateTimeRequest.objects.filter(request_date = cur_date.date,
							 request_start_time__lte = cur_time,
							 request_end_time__gte = cur_time)
	
	# filter requests by unavailable workers
	qs_all_valid_emp_requests = qs_all_requests.exclude(request_employee__in = unavailable_workers)

	# TODO make this a dictionary/map
	all_vacation = []
	all_sick = []
 	all_preferred = []
	all_skip = []

	# group them into their different types
	for one_request in qs_all_requests:
		if (one_request.request_type == one_request.VACATION):
			all_vacation.append(one_request)
		elif (one_request.request_type == one_request.SICK):
			all_sick.append(one_request)
		elif (one_request.request_type == one_request.PREFERRED):
			all_preferred.append(one_request)
		elif (one_request.request_type == one_request.SKIP):
			all_skip.append(one_request)
		else:
			"nothing"

	# ****************************************************************************
	# *** remove all employees from main list that are in cannot work requests ***
	# TODO: Maybe dont need this because we get rid of them based on future even
	
	# Skip requests (cannot work this day)
	if all_skip:
		for skip_request in all_skip:
			if skip_request.request_employee in available_employees:
				available_employees.remove(skip_request.request_employee)

	# Sick requests (im sick or am going to be sick (dr visit))
	if all_sick:
		for sick_request in all_sick:
			if sick_request.request_employee in available_employees:
				available_employees.remove(sick_request.request_employee)

	# Vacation requests (im sick or am going to be sick (dr visit))
	if all_vacation:
		for vacation_request in all_vacation:
			if vacation_request.request_employee in available_employees:
				available_employees.remove(vacation_request.request_employee)

	# ****************************************************************
	# *** add in duplicates in main list for emps with preferences ***

	# Vacation requests (im sick or am going to be sick (dr visit))
	if all_preferred:
		for preferred_request in all_preferred:
			if preferred_request.request_employee in available_employees:
				available_employees.append(preferred_request.request_employee)

	# select random employee from final list and return it
	if available_employees:

		# init return val
		return_val = [None]*2
		
		# get employee
		# TODO: Instead of getting the first get a random available employee
		# once we have stuff down well
		return_val[0] = available_employees[0]
		#return_val[0] = random.choice(available_employees)
		
		# get employee types for chosen employee
		chosen_employee_types = PersonEmployeeType.objects.filter(pet_employee = return_val[0])
		temp_chosen_employee_types = []
		for chosen_employee_type in chosen_employee_types:
			temp_chosen_employee_types.append(chosen_employee_type.pet_employee_type)

		# get list of chosen employee's types and what we need intersected
		chosen_employee_types_intersect = []
		chosen_employee_types_intersect = list(set.intersection(set(temp_chosen_employee_types),set(temp_emp_types_needed)))
		return_val[1] = chosen_employee_types_intersect[0]
		#return_val[1] = random.choice(chosen_employee_types_intersect)

		return return_val
	else:
		return False


'''
****************************************************
  Takes a list of shifts in active_shifts and updates it
  based on requirements and people working enough hours etc

****************************************************
'''
def RemoveActiveShifts(shifts_to_screen,workday,time):	
	
	# ------------------------------
	# remove active shifts based on hours worked
	# and hours available
	#pdb.set_trace()
	"active shifts"
	temp_active_shifts = []
	for active_shift in shifts_to_screen:

		# remove any shifts that have completed their max hour req for the day
		if( active_shift.hours() == active_shift.employee.person_max_hours_per_shift ):
			"prevent from active shift"
		# remove any shifts that the employee can't work the next hour
		# < 2 catches shift that should have ended already (0) and 
		# shift that is going to be over (1); (>=2) means they have at least another hour to work
		elif( HoursUntilCantWork(active_shift.employee,workday.date,time) < 2 ):
			"prevent from active shift"
		else:
			temp_active_shifts.append(active_shift)
	
	# update active shifts list
	shifts_to_screen[:] = []
	shifts_to_screen = temp_active_shifts[:]
	temp_active_shifts[:] = []

	# -----------------------------------
	# remove active shifts based on having a higher number
	# of employees working than are required 
	# remove randomly for now maybe make smart enough to remove
	# workers who've worked more hours (that day or that week)

	# get dict of requirement types keyed by the type of employee (manager, cook, eye dr., etc)
	employee_type_requirements = {}
	employee_type_requirements = GetEmployeeTypeRequirements(workday.date,time)

	if ( not(employee_type_requirements) ):
	
		# cancel all active shifts
		# maybe only cancel them when they have met a min shift requirment
		active_shifts[:] = []
		
	else:
		# if we still have shifts then there is some work to be done still
		if( shifts_to_screen ):

			# for all the shifts, create a map of
			# { Employee_Type , [Shifts] }
			active_shifts_by_employee_type = {}
			for shift in shifts_to_screen:
				if( shift.shift_employee_type.et_type in active_shifts_by_employee_type ):
					active_shifts_by_employee_type[shift.shift_employee_type.et_type].append(shift)
				else:
					active_shifts_by_employee_type[shift.shift_employee_type.et_type] = [shift]
				

			# for all the requirements get the first one and get its count so we have a mapt of
			# { Employee_Type , Count }
			requirement_count_by_employee_type = {}
			for employee_type, requirement_list in employee_type_requirements.items():
				requirement_count_by_employee_type[employee_type] = requirement_list[0].etr_employee_type_count


			# remove any shifts that dont have employee types not in employee requirements
			# and remove any shifts in employee types that have more worker than that are required.
			for employee_type, shift_list in active_shifts_by_employee_type.items():
				if( employee_type in requirement_count_by_employee_type ):
					if( requirement_count_by_employee_type[employee_type] > len(shift_list) ):
						temp_active_shifts += shift_list
					else:
						temp_active_shifts += random.sample(shift_list,requirement_count_by_employee_type[employee_type])
	
			# update active shifts list
			shifts_to_screen[:] = []
			shifts_to_screen = temp_active_shifts[:]
			temp_active_shifts[:] = []
	return shifts_to_screen

'''
****************************************************
Given Person Object, DateTime Date, DateTime Time

return int of number of hours until the employee can't work
given all the "can't work" requests specified (SICK,VACA,SKIP)

****************************************************
'''	
def HoursUntilCantWork(employee,date,time):

	# TODO: https://docs.djangoproject.com/en/1.8/ref/models/querysets/#django.db.models.query.QuerySet.latest
	# TODO: evaluate if 25 is the correct thing to do here or if it just happens to work

	# check to see if there are any requests
	qs_any_requests = DateTimeRequest.objects.filter(
						request_employee = employee,
						request_date = date
						).exclude(
						request_type = 'PREF')
	if( not(qs_any_requests) ):
		return int(25 - time.hour)

	# check to see if the current time is currently in a request's time slot
	qs_during_requests = DateTimeRequest.objects.filter(
						request_employee = employee,
						request_date = date,
						request_start_time__lte = time,
						request_end_time__gt = time
						).exclude(
						request_type = 'PREF')
	if( qs_during_requests ):
		return 0

	# check to see if there are any future requests
	qs_future_request = DateTimeRequest.objects.filter(
						request_employee = employee,
						request_date = date,
						request_start_time__gte = time
						).exclude(
						request_type = 'PREF'
						).order_by(
						"-request_start_time").first()
	if( qs_future_request ):
		return int(qs_future_request[0].request_start_time.hour - time.hour)

	return int(25 - time.hour)
	
					


'''
****************************************************

****************************************************
'''	
def Log_Schedule_Error(error_key,error_info):
	Log_Error(error_key,str(error_info))



'''
****************************************************

****************************************************
'''	
def Log_Error(key,value):

	global make_schedule_errors

	if not key in make_schedule_errors:
        	make_schedule_errors[key] = [value]
    	else:
        	make_schedule_errors[key].append(value)

