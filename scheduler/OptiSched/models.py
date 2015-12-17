import datetime
import time

from django.db import models
from django.utils import timezone 

# Create Shift Error logging
# Date and Error Code (internal / external)

class Person(models.Model):
	
	first_name = models.CharField(max_length=60)
	last_name = models.CharField(max_length=60)

	# min max hours to work per week
	person_min_hours_per_week = models.IntegerField(default=25)
	person_max_hours_per_week = models.IntegerField(default=40)

	# min max hours to work per shift
	person_min_hours_per_shift = models.IntegerField(default=4)
	person_max_hours_per_shift = models.IntegerField(default=8)

	def name(self):
        	return ''.join([self.last_name,',', self.first_name])

	def __str__(self):             	
	        #return str(self.name()) + ' (id: ' + str(self.id) + ')'
		return str(self.name())

class PersonEmployeeType(models.Model):
	
	# employee
	pet_employee = models.ForeignKey(Person)

	# employee type
	pet_employee_type = models.ForeignKey('EmployeeType')

	# Members
	
	def __str__(self):
		return str(self.pet_employee) + ' ' + str(self.pet_employee_type)


class Shift(models.Model):

	# date for shift
	shift_date = models.ForeignKey('Date')
	
	# employee on shift	
	employee = models.ForeignKey(Person)

	# Employee Type for employee
	# TODO: Limit choices to the employee's employee types?
	shift_employee_type = models.ForeignKey('EmployeeType')
    
    	start_time = models.TimeField("Start Time")
	end_time = models.TimeField("End Time")

	def hours(self):
		start_hours = self.start_time.hour
		end_hours = self.end_hour()
		duration = end_hours - start_hours
		return abs(duration)

	def end_hour(self):
		
		if (self.end_time.hour == 23 and
		    self.end_time.minute > 0 ):
			end_hours = 24
		elif (self.end_time.hour == 0 and
		      self.end_time.minute == 0):
			end_hours = 24
		elif (self.end_time.hour == 0 and
		      self.end_minute > 0):
			end_hours = 1
		else:
			end_hours = self.end_time.hour
		return end_hours
		
	def hour_list(self):
		return list(range(self.start_time.hour,self.end_hour()))

	def hours_disp(self):
		return str(self.hours())		

	def get_week(self):
		return self.shift_date.date.isocalendar()[1]
	get_week.short_description = "week"

	def display_details(self):
		return str(self.employee.name()) + ' Position: ' + str(self.shift_employee_type) + ' For: ' + self.hours_disp() + ' hours'

	def __str__(self):
		return self.display_details()

class Date(models.Model):
	date = models.DateField(primary_key=True,
			        default=datetime.date.today)
	# Schedule Params
	day_start_time = models.TimeField("Day Start Time",
				          default = datetime.time(8,0,0))
	day_end_time = models.TimeField("Day End Time",
				        default = datetime.time(23,59,0))
	
	def total_hours(self):
		start_hours = self.day_start_time.hour
		if (self.day_end_time.hour == 23 and
		    self.day_end_time.minute > 0 ):
			end_hours = 24
		elif (self.day_end_time.hour == 0 and
		      self.day_end_time.minute == 0):
			end_hours = 24
		elif (self.day_end_time.hour == 0 and
		      self.day_end_minute > 0):
			end_hours = 1
		else:
			end_hours = self.day_end_time.hour
		duration = end_hours - start_hours
		return abs(duration)

	# is holiday YN BooleanField property
	def day_of_week(self):
		dow = self.date.weekday()
    		if dow == 0:
        		dow = 'Monday'
    		elif dow == 1:
        		dow = 'Tuesday'
    		elif dow == 2:
        		dow = 'Wednesday'
    		elif dow == 3:
        		dow = 'Thursday'
    		elif dow == 4:
        		dow = 'Friday'
    		elif dow == 5:
        		dow = 'Saturday'
    		elif dow == 6:
        		dow = 'Sunday'
    		else:
        		dow = 'Undefined'
		return dow		

	def week(self):
		return self.date.isocalendar()[1]

	def date_display(self):
        	 return self.day_of_week() + ' ' + str(self.date) + ' ' + 'week: ' + str(self.week())

	def __str__(self):
		return str(self.date)
'''
TODO: Allow to specify typical days that employees request off such as every 
	tuesday a certain employee cannot work (so starting at (0,0,0)
	or every tuesday an employee only works morning not noon so (12,0,0)

class DayTimeRequest(models.Model):

	DAYS_OF_WEEK = (
			(0,'Monday'),
			(1,'Tuesday'),
			(2,'Wednesday'),
			(3,'Thursday'),
			(4,'Friday'),
			(5,'Saturday'),
			(6,'Sunday'),
			)
	
	REQUEST_TYPES = (
        		  (PREFERRED, 'Preferred'),
        		  (SKIP, 'Cannot Work'),
    			 )

	# employee key
	dtr_employee = models.ForeignKey(Person)

	# Day of the week
	dtr_day_of_week = models.IntegerField(choices = DAYS_OF_WEEK)

	# Request
    	dtr_request_type = models.CharField(max_length=4, choices=REQUEST_TYPES)

	# Time the req should start
	dtr_start_time = models.TimeField("Request Start Time",
				          default = datetime.time(0,0,0))
	# Time the req should stop
	dtr_end_time = models.TimeField("Request End Time",
				          default = datetime.time(23,59,0))

	class Meta:
		unique_together = (("dtr_employee","dtr_day_of_week"),)

	# Members
	def __str__(self):
		return str(self.dtr_employee) + ' ' + str(self.dtr_day_of_week) + ' ' + str(self.dtr_start_time.strftime("%H:%M")) + " " +  str(self.dtr_request_type)

'''

class DateTimeRequest(models.Model):
	# There are going to be serveral of these if a vaca spans multiple days 

	# date key
	# TODO: maybe need to make this required somehow
	request_date = models.DateField()

	# employee key
	request_employee = models.ForeignKey(Person)

	# start and end times
	request_start_time = models.TimeField("Request Start Time",
				              default = datetime.time(0,0,0))
	request_end_time = models.TimeField("Request End Time",
				            default = datetime.time(23,59,0))
	
	# store request types
	VACATION = 'VACA'
	SICK = 'SICK'
	PREFERRED = 'PREF'
	SKIP = 'SKIP'
	
	REQUEST_TYPES = (
        		  (VACATION, 'Vacation'),
        		  (SICK, 'Sick'),
        		  (PREFERRED, 'Preferred'),
        		  (SKIP, 'Cannot Work'),
    			 )

    	request_type = models.CharField(max_length=4, choices=REQUEST_TYPES)

	# Members
	def displayRequestDateSpan(self):
		return str(self.request_date) + ' ' + str(self.request_start_time) + ' - ' + str(self.request_end_time)

	def __str__(self):
		return str(self.request_employee) + ' ' + self.displayRequestDateSpan() + ' ' + self.get_request_type_display()

class EmployeeType(models.Model):
	
	# employee type
	et_type = models.CharField(primary_key=True,max_length=60)

	# Members
	def __str__(self):
		return str(self.et_type)

class EmployeeTypeRequirement(models.Model):
	
	# Employee Type
	etr_employee_type = models.ForeignKey(EmployeeType)

	# Count for Employee Type
	etr_employee_type_count = models.IntegerField()

	class Meta:
		unique_together = (("etr_employee_type","etr_employee_type_count"),)

	# Members
	def __str__(self):
		return str(self.etr_employee_type) + ' ' + str(self.etr_employee_type_count)

class EmployeeRequirementDateTimeOverride(models.Model):

	# DateTime
	erd_datetime = models.DateTimeField()

	# Requirement
	erd_requirement = models.ForeignKey(EmployeeTypeRequirement)

	class Meta:
		unique_together = (("erd_datetime","erd_requirement"),)

	# Members
	def __str__(self):
		return str(self.erd_datetime.strftime("%Y-%m-%d %H:%M")) + " " +  str(self.erd_requirement)

class EmployeeRequirementTime(models.Model):

	days_of_week = (
			(0,'Monday'),
			(1,'Tuesday'),
			(2,'Wednesday'),
			(3,'Thursday'),
			(4,'Friday'),
			(5,'Saturday'),
			(6,'Sunday'),
			)

	# Day of the week
	day_of_week = models.IntegerField(choices = days_of_week)

	# Time the req should take effect
	ert_start_time = models.TimeField("Effective Hour",
				          default = datetime.time(0,0,0))

	# Requirement
	ert_requirement = models.ForeignKey(EmployeeTypeRequirement)

	class Meta:
		unique_together = (("day_of_week","ert_start_time","ert_requirement"),)

	# Members
	def __str__(self):
		return str(self.day_of_week)+ ' ' + str(self.ert_start_time.strftime("%H:%M")) + " " +  str(self.ert_requirement)



	



