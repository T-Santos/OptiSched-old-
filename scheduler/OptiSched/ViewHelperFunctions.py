import datetime as dt

import ScheduleDateTimeUtilities

def ConvertErrorsToGroups(errors,time_slice_amt):

	'''
		map of 
		{ employee type: [errors associated early to late]}
	'''
	error_groups = {}

	errors = errors.order_by('error_emp_type','-error_time')
	for error in errors:
		if error.error_emp_type.et_type in error_groups:
			error_groups[error_emp_type.et_type].append(error)
		else:
			error_groups[error_emp_type.et_type] = [error]

	return error_groups