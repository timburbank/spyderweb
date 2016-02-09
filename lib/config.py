# Functions for reading config files, wherever those
# config files happen to be

# This might need some kind of reference to the evironment

def fields(env):
	
	# note: id will always be a field
	fields = ['name', 'description', 'status']

	fields.insert(0, 'id')
	return(fields)
