# Functions for interacting with the database

import os
from . import config

env = "data env"

# params
# fields: list of ticket fields to retrieve, if unspecified reads config
# filters: list of lists of [field, value, comparison]
# order: string, field to order by
# limit: int, how many items to retrieve
# ascending: bool, which way to order
#
# return
# list of dicts of ticket data
def get_ticket_data(fields = None, filters = 0, order='id', ascending = 1, limit = 0):
	#TODO: order, ascending, limit
	
	ticket_listception = []
	
	# Cheat and only retrieve one file if it's filtered by ID,
	# otherwise get all data from all ticket files
	try:
		if filters[0][0] == 'id':
			i = filters[0][1]
			filter_by_id = True
		else:
			i = 1
			filter_by_id = False
	except:
		i = 1
		filter_by_id = False
		
	file_path = os.path.join(env, '{}.spy'.format(i))
	while(os.path.isfile(file_path)):
		read_file = open(file_path)
		file_contents = read_file.read()
		read_file.close()
		ticket_data = []
		for field in file_contents.split('{'):
			ticket_data.append(field.split('}'))

		ticket_data.append(['id', i])
		# don't include header in ticket fields
		ticket_listception.append(ticket_data[1:])
		
		if filter_by_id:
			break

		i += 1
		file_path = os.path.join(env, '{}.spy'.format(i))

		

	ticket_list = []

	# copy data to dictionary
	for ticket in ticket_listception:
		ticket_dict = {}
		
		if fields is None:
			retrieval_fields = config.fields() + ['id']
		else:
			retrieval_fields = fields + ['id']

		for field in retrieval_fields:
			field_exists = False
			for ticket_field in ticket:
				if ticket_field[0] == field:
					ticket_dict[field] = str(ticket_field[1]).strip()
					field_exists = True

			if not field_exists:
				ticket_dict[field] = config.field_default(field)

		# filter data. could maybe be combined with above bit, but this is 
		# the lazy version 
		pass_filters = True
		if filters:
			for filter in filters:
				key = str(filter[0]).strip()
				filter_value = str(filter[1]).strip()
				try:
					ticket_field_value = str(ticket_dict[key]).strip()
				except KeyError as err:
					print("Key error:{} \n".format(err) + \
					      "Make sure the layout in spyderweb.ini doesn't " + \
						  "reference a field that's not in [ticket_fields]")
					exit()

				try:
					comparison = filter[2]
				except:
					comparison = '='

				if comparison is '=' and ticket_field_value != filter_value:
					pass_filters = False
				elif comparison is 'not' and ticket_field_value == filter_value:
					pass_filters = False
		if pass_filters:
			ticket_list.append(ticket_dict)

	return(ticket_list)


# Returns highest version number of ticket
def get_version(ticket_id):
	return(0)


# Writes ticket data to storage
# 
# param:
# data, library of key:value pairs to store
# id, int ID of ticket to write
def set_ticket_data(ticket_id, data):
	file_path = os.path.join(env, '{}.spy'.format(ticket_id))

	# Need to determine if field already exists
	# read in exsting data as list of lists so it remains ordered 
	existing_fields = []
	
	if os.path.isfile(file_path):
		ticket_read_file = open(file_path, 'r')
		file_contents = ticket_read_file.read()
		ticket_read_file.close()

		for field in file_contents.split('{'):
			existing_fields.append(field.split('}'))

	for field, content in data.items():
		if field != "id":
			# check default values if nothing provided
			if content == '':
				content = config.field_default(field)

			if content is not '':	
				# if a data field exists in the list update it
				exists = False
				formatted_content = '\n{}\n\n'.format(content)
				for existing_field in existing_fields:
					if existing_field[0] == field:
						existing_field[1] = formatted_content
						exists = True

				# if it doesn't exist append it to the list
				if exists == False:
					existing_fields.append([field, formatted_content])

	# reformat everything and write back to a file
	new_contents = 'spyderweb text 1\n\n'
	for i in range(1, len(existing_fields)):
		new_contents += '{' + existing_fields[i][0] + '}' + \
					     existing_fields[i][1]

	ticket_write_file = open(file_path, 'w')
	ticket_write_file.write(new_contents)
	ticket_write_file.close()
	return(True)


# Creates new ticket
#
# param:
# data, library of key:value pairs for new ticket
#
# return: id
def create_ticket(data):
# figure out highest existing id
	id_num = 1
	while os.path.exists(os.path.join(env, '{}.spy'.format(id_num))):
		id_num += 1

	new_file = open(os.path.join(env, '{}.spy'.format(id_num)), 'w')
	new_file.close()
	set_ticket_data(id_num, data)
	print('create_ticket() id: {}'.format(id_num))
	return(id_num)
	
	


# write header "spyderweb text 1"

# write each field


# setup database
def initialize():
	print('initialize() is not implemented in data_text.py')
	return(None)


def delete(ticket_id):
	print('delete() is not implemented in data_text.py')
	return(None)

def hide(ticket_id):
	print('hide() is not implemented in data_text.py')
	return(None)


def unhide(ticket_id):
	print('unhide() is not implemented in data_text.py')
	return(None)


# update possible previous versions of the database
def upgrade():
	print('upgrade() is not implemented in data_text.py')
	return(None)
