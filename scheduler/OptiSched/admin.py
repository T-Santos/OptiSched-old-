from django.contrib import admin

from .models import Date,Person,Shift

#admin.site.register(Shift)
#dmin.site.register(Person)

class ShiftAdmin(admin.ModelAdmin):

	list_display = ('employee','shift_date','hours')
	search_fields = ('employee.last_name','employee.first_name')

class PersonAdmin(admin.ModelAdmin):

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
admin.site.register(Date, DateAdmin)
admin.site.register(Person,PersonAdmin)
