from django.contrib import admin

from OptiSched.models import *

class ShiftAdmin(admin.ModelAdmin):

	list_display = ('employee','shift_date','get_week','hours')
	search_fields = ('employee.last_name','employee.first_name')

class PersonAdmin(admin.ModelAdmin):
	
	list_display = ('id','name')
	search_fields = ['id','last_name','first_name']

class ShiftInline(admin.TabularInline):
    model = Shift
    extra = 0

class DateAdmin(admin.ModelAdmin):

	model = Date	
	list_filter = ['date']
	search_fields = ['date']
	list_display = ('date_display', 'date','week','day_of_week')

    	inlines = [ShiftInline]

admin.site.register(Shift,ShiftAdmin)
admin.site.register(Date,DateAdmin)
admin.site.register(Person,PersonAdmin)

admin.site.register(EmployeeType)
admin.site.register(PersonEmployeeType)
admin.site.register(EmployeeTypeRequirement)

admin.site.register(RequirementDayTime)
admin.site.register(RequirementDateTime)

admin.site.register(RequestDayTime)
admin.site.register(RequestDateTime)

admin.site.register(EmployeeTypeShiftError)
