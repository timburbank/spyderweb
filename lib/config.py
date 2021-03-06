# Functions for reading config files, wherever those
# config files happen to be
import os

from sys import version_info
py3 = version_info[0] > 2
if py3:
	import configparser
else:
	import ConfigParser as configparser 

env = ""

def get_value_list(section, option):
# note: id will always be a field
# maybe it's weird for this to return list?

# based on https://pymotw.com/2/ConfigParser/
## setup, should maybe be moved to it's own fuction 
	config_file = os.path.join(env, 'spyderweb.ini')
	try:
		parser = configparser.SafeConfigParser(allow_no_value=True)
		parser.read(config_file)
	except configparser.ParsingError as err:
		print('Could not parse:' + err)
	## end setup
	fields_csv = parser.get(section, option)
	# default to empty string if unset
	if fields_csv == None:
		fields_csv = ''
	fields = fields_csv.split(',')
	clean_fields = list(map(str.strip, fields))
						

	return(clean_fields)

def fields():
	## setup
	config_file = os.path.join(env, 'spyderweb.ini')
	try:
		parser = configparser.SafeConfigParser(allow_no_value=True)
		parser.read(config_file)
	except configparser.ParsingError as err:
		print('Could not parse:' + err)
	## end setup

	fields = parser.options('ticket_fields')
	return(fields)

# returns fields shown when listing tickets (can maybe take
# optional param for different views?)
def list_fields(layout='default'):
	config_data = get_value_list('list-{}'.format(layout), 'columns')
	# config items are stored as "field_name:column_width"
	list_fields = [field.split(':') for field in config_data]
	return(list_fields)

def field_type(field):
	field_type = get_value_list('field_input_types', field)[0]
	return(field_type)

def field_default(field):
	field_default = get_value_list('ticket_fields', field)[0]
	return(field_default)

def data_storage():
	data_storage = get_value_list('config', 'data_storage')[0]
	return(data_storage)


# return the list of filters for a given layout,
# combining show_only and hide parameters
def list_filters(layout='default'):
	try:
		config_data = get_value_list('list-{}'.format(layout), 'show_only')
		show = [field.split(':') for field in config_data]
	except configparser.NoOptionError:
		show = []

	for item in show:
		item.append('=')

	try:
		config_data = get_value_list('list-{}'.format(layout), 'hide')
		hide = [field.split(':') for field in config_data]
	except configparser.NoOptionError:
		hide = []

	for item in hide:
		item.append('not')

	return(show + hide)

def time_list_field():
	list_field = get_value_list('time', 'list_field')[0]
	return(list_field)


def initialize():
	from shutil import copyfile

	config_file = os.path.join(env, 'spyderweb.ini')
	default_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), \
	                            '../env/spyderweb.ini')
	copyfile(default_file, config_file)
