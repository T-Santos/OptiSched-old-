from django.conf.urls import url

from . import views

urlpatterns = [

	# ------ Navigation ------

	# ex: /OptiSched/
	url(r'^$', views.index, name='index'),

	#TODO: /OptiSched/Weeks/   (This should iterate weeks that then break down a week date)

	#TODO: /OptiSched/Days/    (This should iterate days that then link to OptiSched/<Date>)

	# ------ Views --------

	# /OptiSched/Employees/
	url(r'^Employees/$', views.employees, name='employees'),

	# ex: /OptiSched/<Date>/Week
	url(r'^Week/(?P<date>\d{4}-\d{2}-\d{2})/$', views.week, name='week'),

	# ex: /OptiSched/<Date>/
    	url(r'^(?P<date>\d{4}-\d{2}-\d{2})/$', views.day, name='day'),

    	# ex: /OptiSched/<Date>/<Employee_Id>/
    	url(r'^(?P<date>\d{4}-\d{2}-\d{2})/(?P<Person_id>[0-9]+)/$', views.day_person, name='day_person'),

	# ------ Action -------

	# ex: /OptiSched/CreateSchedule/	
	url(r'^CreateSchedule/$', views.create_schedule, name='create_schedule'),	
	
	# ------- Testing ------

	# /OptiSched/TestButton/
	url(r'^TestButton/$', views.button, name='button'),

]

# (19|20)\d\d[- /.](0[1-9]|1[012])[- /.](0[1-9]|[12][0-9]|3[01])
# (?P<date1>\d{2}-\d{2}-\d{4})