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
	#TODO: filters, order, ascending, limit
	print('get_ticket_data')
	print('fields:{}'.format(fields))
	print('filters:{}'.format(filters))
	
	ticket_listception = []
	# check for special case, if filtered for id, so we don't have
	# to read every single file if we know what we're looking for
	if filters[0][0] == 'id':
		read_file = open(os.path.join(env, '{}.spy'.format(filters[0][1])))
		file_contents = read_file.read()
		read_file.close()
		ticket_data = []
		for field in file_contents.split('{'):
			ticket_data.append(field.split('}'))

		ticket_data.append(['id', filters[0][1]])
		# dont' include header in ticket fields
		ticket_listception.append(ticket_data[1:])

		

	# TODO: handle other cases
	
	# get all data from all ticket files
	else:
		i = 1
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
			
			i += 1
			file_path = os.path.join(env, '{}.spy'.format(i))

		

	ticket_list = []

	# copy data to dictionary
	for ticket in ticket_listception:
		ticket_dict = {}
		
		if fields is None:
			fields = config.fields()

		fields.append('id')
		for field in fields:
			field_exists = False
			for ticket_field in ticket:
				if ticket_field[0] == field:
					ticket_dict[field] = str(ticket_field[1]).strip()
					field_exists = True

			if not field_exists:
				ticket_dict[field] = config.field_default(field)

		ticket_list.append(ticket_dict)
		
	return(ticket_list)


# Returns highest version number of ticket
def get_version(ticket_id):
	print('get_Version')
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
	return(id_num)
	
	


# write header "spyderweb text 1"

# write each field


# setup database
def initialize():
	print('initialize')
	return(None)


def delete(ticket_id):
	print('delete')
	return(None)

def hide(ticket_id):
	print('hide')
	return(None)


def unhide(ticket_id):
	print('unhide')
	return(None)


# update possible previous versions of the database
def upgrade():
	print('upgrade')
	return(None)