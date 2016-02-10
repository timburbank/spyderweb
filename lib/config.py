# Functions for reading config files, wherever those
# config files happen to be

env = ""

# This might need some kind of reference to the evironment

def fields():
	
	# note: id will always be a field
	fields = ['name', 'description', 'status']

	return(fields)


# returns fields shown when listing tickets (can maybe take
# optional param for different views?)
def list_fields():
	list_fields = ['id', 'name', 'status']
	return(list_fields)

