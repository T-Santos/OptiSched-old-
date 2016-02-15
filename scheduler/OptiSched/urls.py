from django.conf.urls import url

from . import views

'''

o When capturing ags in the url, they need to have the same name
  as whats being received in the views.py def for that view
'''

urlpatterns = [

	# ------ Main Pages -------
	url(r'^$', views.home, name='home'),
	url(r'^Home/', views.home, name='home'),
	url(r'^About/$', views.about, name='about'),
	url(r'^Contact/$', views.contact, name='contact'),
	url(r'^Dashboard/$', views.dashboard, name='dashboard'),

	# ------ Actions ---------
	url(r'^CreateSchedule/$', views.create_schedule, name='create_schedule'),
	url(r'^CreateDateSpan/$', views.create_date_span, name='create_date_span'),

	# ------ Navigation ------
	url(r'^ViewManagerDay/', views.ViewManagerDay, name='ViewManagerDay'),
	url(r'^ViewEmployeeWeek/(?P<employee_id>[0-9]+)/(?P<date>\d{4}-\d{2}-\d{2})/$', views.ViewEmployeeWeek, name='ViewEmployeeWeek'),

]
