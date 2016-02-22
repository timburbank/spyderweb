# Functions for reading config files, wherever those
# config files happen to be
import os
import ConfigParser

env = ""

# This might need some kind of reference to the evironment

def get_value(section, option):
	# note: id will always be a field
	
	# based on https://pymotw.com/2/ConfigParser/
	config_file = os.path.join(env, 'spyderweb.conf')	
	try:
		parser = ConfigParser.SafeConfigParser()
		parser.read(config_file)
	except ConfigParser.ParsingError, err:
		print 'Could not parse:', err

	fields_csv = parser.get(section, option)
	
	fields = fields_csv.split(',')
	clean_fields = map(str.strip, fields)
	
	return(clean_fields)

def fields():
	fields = get_value('tickets', 'fields')
	return(fields)

# returns fields shown when listing tickets (can maybe take
# optional param for different views?)
def list_fields():
	list_fields = get_value('list', 'list_fields')
	return(list_fields)

